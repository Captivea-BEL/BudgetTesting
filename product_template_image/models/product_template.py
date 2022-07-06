# -*- coding: utf-8 -*-

from odoo import api, models, fields
import logging
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'    
    
    img_url = fields.Char('img url')

    @api.model
    def get_http(self):
        return True

    