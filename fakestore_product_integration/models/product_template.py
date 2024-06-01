from odoo import models, fields, api
import requests
from odoo.exceptions import ValidationError
import base64
import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"

    rating_rate = fields.Float(string="Rating Rate")
    rating_count = fields.Integer(string="Rating Count")
    image_url = fields.Char("Image URL")
    api_product = fields.Boolean(default=False)
    custom_id = fields.Char(string='Custom ID')

    @api.onchange("image_1920")
    def _onchange_image_1920(self):
        """
        Clear the image_url field when image_1920 is changed.

        This method is triggered whenever the image_1920 field is modified.
        If image_1920 has a value, it resets the image_url field to indicate
        that the product image has been edited. This allows the scheduled action
        to know that the image needs to be updated with data from the API.
        """
        if self.image_1920:
            self.image_url = False

    @api.model
    def _cron_update_products_from_api(self):
        """
        Update products from the Fake Store API.

        This method fetches the latest product data from the configured API URL
        and creates or updates products in Odoo based on the data.
        It is intended to be used as a scheduled action that executes
        daily.

        Returns:
            None
        """

        if not self._is_api_enabled():
            return

        products = self._fetch_product_data_from_api()

        for product_data in products:
            try:
                self._create_or_update_product(product_data)
            except Exception as e:
                raise ValidationError(f"Error creating or updating product: {e}")

    def _is_api_enabled(self):
        """
        Check if the API is enabled and the URL is configured.

        Returns:
            bool: True if the API is enabled and URL is set, False otherwise.
        """
        company = self.env.user.company_id
        return company.api_enabled and company.api_url

    def _fetch_product_data_from_api(self):
        """
        Fetch product data from the API.

        Returns:
            list: List of product data dictionaries.
        """
        company = self.env.user.company_id

        # Validate that the API URL is configured
        if not company.api_url:
            raise ValidationError("The API URL is not configured in the company settings.")

        try:
            
            response = requests.get(company.api_url)
            response.raise_for_status()
        except requests.RequestException as e:
            raise ValidationError(f"Error fetching data from API: {e}")

        if response.status_code != 200:
            raise ValidationError(
                f"Failed to fetch data from API. Status code: {response.status_code}"
            )
        return response.json()

    def _create_or_update_product(self, product_data):
        """
        Create or update a product record based on provided data from an API.

        Args:
            product_data (dict): Dictionary containing product data retrieved from an external API.

        Returns:
            None
        """
        category = self._get_or_create_category(product_data.get("category"))
        product = self.env["product.template"].search(
            [("custom_id", "=", str(product_data.get("id")))], limit=1
        )
    
        values = self._prepare_product_values(product_data, category)

        new_image_url = product_data.get("image")
        
        if product:
            if new_image_url and new_image_url != product.image_url:
                try:
                    new_image = self.get_image_from_url(new_image_url)
                    if new_image:
                        values["image_1920"] = new_image
                except ValidationError as e:
                    _logger.error(f"Error updating image for product {product_data.get('id')}: {e}")
            product.with_context(lang=self.env.user.lang).write(values)
            product.write(values)
        else:
            if new_image_url:
                try:
                    image_response = self.get_image_from_url(new_image_url)
                    if image_response:
                        values["image_1920"] = image_response
                except ValidationError as e:
                    _logger.error(f"Error downloading image for new product {product_data.get('id')}: {e}")
                    
            self.create(values)


    def _get_or_create_category(self, category_name):
        """
        Retrieve an existing product category by name or create 
        a new one if it does not exist.

        Args:
            category_name (str): The name of the category to search 
            for or create.

        Returns:
            recordset: A recordset of the product category.
        """
        category = self.env["product.category"].search(
            [("name", "=", category_name)], limit=1
        )
        if not category:
            category = self.env["product.category"].create({"name": category_name})
        return category

    def _prepare_product_values(self, product_data, category):
        """
        Prepare the values needed to create or update a product record.

        Args:
            product_data (dict): Dictionary containing product data from an external source.
            category (recordset): A recordset of the product category.

        Returns:
            dict: A dictionary of values to create or update a product record.
        """
        rating_data = product_data.get("rating", {})
        values = {
            "custom_id":  product_data.get("id", "Default id"),
            "name": product_data.get("title", "Default Title"),
            "list_price": product_data.get("price", 0.0),
            "categ_id": category.id,
            "description_sale": product_data.get("description", ""),
            "rating_rate": rating_data.get("rate", 0.0),
            "rating_count": rating_data.get("count", 0.0),
            "api_product": True,
            "image_url": product_data.get("image"),
        }
        return values


    def get_image_from_url(self, url: str):
        """
        Download an image from a URL and return its content in base64 format.

        Args:
            url (str): The URL of the image.

        Returns: The content of the image in base64 if the download is successful,
                    or False if any error occurs.
        """
        try:
            with requests.get(url, timeout=5) as response:
                if response.status_code == 200:
                    return base64.b64encode(response.content)
                else:
                    raise ValidationError(
                        f"Failed to download image from URL: {url}. Status code: {response.status_code}"
                    )
        except requests.RequestException as e:
            raise ValidationError(f"Error downloading image from URL: {url}. {e}")
