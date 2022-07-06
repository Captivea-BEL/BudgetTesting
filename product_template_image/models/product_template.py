# -*- coding: utf-8 -*-

from odoo import api, models, fields
from odoo.exceptions import UserError
import logging
import base64
import requests
_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'    
    
    img_url = fields.Char('img url')

    def get_http(self):
        url = self.img_url
        var = base64.b64encode(requests.get(url).content)
        self.image_1920 = var


