from odoo import http
from odoo.http import request
from werkzeug.wrappers import Response
import io
import xlsxwriter


class ExcelDownloadController(http.Controller):
    """Controller for exporting products to Excel."""

    @http.route("/download/excel", type="http", auth="user")
    def export_products_excel_from_api(self, **kwargs):
        """
        Export products data to Excel and return as HTTP response.

        Args:
            **kwargs: Additional keyword arguments (not used).

        Returns:
            Response: HTTP response with the Excel file.
        """
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output)

        # Create styles
        styles = self._create_styles(workbook)

        # Add worksheet and set columns
        sheet = self._setup_worksheet(workbook, styles)

        # Write headers
        self._write_headers(sheet, styles)

        # Write product data
        self._write_product_data(sheet, styles)

        workbook.close()
        output.seek(0)

        # Return the file as a HTTP response
        return self._create_response(output)

    def _create_styles(self, workbook):
        """
        Define and return the styles to be used in the Excel workbook.

        Args:
            workbook (xlsxwriter.Workbook): Workbook object for the Excel file.

        Returns:
            dict: Dictionary containing defined styles.
        """
        styles = {
            "header_title": workbook.add_format(
                {
                    "font_size": 13,
                    "font_name": "Liberation Sans",
                    "align": "center",
                    "text_wrap": True,
                    "bottom": True,
                    "top": True,
                    "left": True,
                    "right": True,
                    "bold": True,
                    "bg_color": "#507AAA",
                    "color": "#FFFFFF",
                }
            ),
            "row_center_style": workbook.add_format(
                {
                    "font_size": 13,
                    "align": "center",
                    "text_wrap": True,
                    "bold": False,
                    "font_name": "Liberation Sans",
                    "color": "#000000",
                }
            ),
            "date_style": workbook.add_format(
                {
                    "font_size": 13,
                    "font_name": "Liberation Sans",
                    "align": "center",
                    "text_wrap": True,
                    "bottom": True,
                    "top": True,
                    "left": True,
                    "right": True,
                    "bold": True,
                }
            ),
            "column_style": workbook.add_format(
                {"font_size": 11, "align": "left", "text_wrap": True}
            ),
        }
        return styles

    def _setup_worksheet(self, workbook, styles):
        """
        Setup worksheet and return the sheet object.

        Args:
            workbook (xlsxwriter.Workbook): Workbook object for the Excel file.
            styles (dict): Dictionary containing defined styles.

        Returns:
            xlsxwriter.worksheet.Worksheet: Worksheet object for the Excel file.
        """
        sheet = workbook.add_worksheet("REPORT PRODUCT TEMPLATE")
        sheet.set_column("A:A", 70, styles["column_style"])
        sheet.set_column("B:B", 15, styles["column_style"])
        sheet.set_column("C:C", 25, styles["column_style"])
        sheet.set_column("D:D", 15, styles["column_style"])
        sheet.set_column("E:E", 15, styles["column_style"])
        sheet.set_column("F:F", 80, styles["column_style"])

        sheet.merge_range(
            "A1:F1", request.env.user.company_id.name, styles["header_title"]
        )
        sheet.merge_range("A3:F3", "PRODUCT TEMPLATE REPORT", styles["header_title"])
        sheet.freeze_panes(6, 0)
        return sheet

    def _write_headers(self, sheet, styles):
        """
        Write headers to the worksheet.

        Args:
            sheet (xlsxwriter.worksheet.Worksheet): Worksheet object for the Excel file.
            styles (dict): Dictionary containing defined styles.
        """
        headers = ["TITLE", "PRICE", "CATEGORY", "RATE", "COUNT", "DESCRIPTION"]
        for col_num, header in enumerate(headers):
            sheet.write(5, col_num, header, styles["header_title"])

    def _write_product_data(self, sheet, styles):
        """
        Write product data to the worksheet.

        Args:
            sheet (xlsxwriter.worksheet.Worksheet): Worksheet object for the Excel file.
            styles (dict): Dictionary containing defined styles.
        """
        products = request.env["product.template"].search([("api_product", "=", True)])
        row_num = 6
        for product in products:
            sheet.write(
                row_num, 0, product.name or "NAME NOT FOUND", styles["row_center_style"]
            )
            sheet.write(
                row_num, 1, product.list_price or 0.0, styles["row_center_style"]
            )
            sheet.write(
                row_num,
                2,
                product.categ_id.name or "CATEGORY NOT FOUND",
                styles["row_center_style"],
            )
            sheet.write(
                row_num, 3, product.rating_rate or 0.0, styles["row_center_style"]
            )
            sheet.write(
                row_num, 4, product.rating_count or 0.0, styles["row_center_style"]
            )
            sheet.write(
                row_num,
                5,
                product.description_sale or "DESCRIPTION NOT FOUND",
                styles["row_center_style"],
            )
            row_num += 1

    def _create_response(self, output):
        """
        Create a HTTP response with the Excel file.

        Args:
            output (io.BytesIO): BytesIO object containing the Excel file.

        Returns:
            Response: HTTP response with the Excel file.
        """
        response = Response(
            output,
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            direct_passthrough=True,
        )
        response.headers.add(
            "Content-Disposition", "attachment", filename="Report_Product_Template.xlsx"
        )
        return response
