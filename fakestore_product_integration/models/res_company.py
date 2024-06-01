# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = 'res.company'

    api_url = fields.Char(string="API URL", default="https://fakestoreapi.com/products")
    api_enabled = fields.Boolean(string="Enable API", default=False)
