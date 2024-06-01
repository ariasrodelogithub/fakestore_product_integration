# -*- coding: utf-8 -*-
{
    'name': 'Fakestore_product_integration',
    'version': '17.0.1.0',
    'description': """ 
        This module integrates products from the Fake Store API into Odoo. 
        Allows creation and updating of products based on data retrieved from the API. 
        Products are automatically updated daily. Additionally, this module provides configuration 
        options to enable/disable API. 
    """,
    'summary': """ Integration with Fake Store API for automatic product creation and updates in Odoo.""",
    'author': 'Mauricio Arias Rodelo',
    'category': 'Integration',
    'depends': ['base', 'website', 'product', 'stockg'],
    "data": [
        "views/res_company_views.xml",
        "views/product_template_views.xml",
        "views/website_template.xml",
        "data/ir_cron_update_products.xml",
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
