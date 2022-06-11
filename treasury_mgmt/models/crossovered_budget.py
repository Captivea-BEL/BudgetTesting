# -*- coding: utf-8 -*-
######################################################################################
#
#    Captivea LLC
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################

from odoo import models, fields, api
from odoo.exceptions import UserError
import logging
_logger = logging.getLogger(__name__)

class Budget(models.Model):
    _inherit = 'crossovered.budget.lines'


    draft_burden = fields.Float(string='Draft Burden', compute="compute_draft_burden",
                                 help="TODO Help Text")
    approved_burden = fields.Float(string='Approved Burden', compute="compute_approved_durden",
                                  help="TODO Help Text")
    released_burden = fields.Float(string='Released Burden', compute="compute_released_burden",
                                  help="TODO Help Text")
    closed_burden = fields.Float(string='closed Burden', compute="compute_closed_burden",
                                  help="TODO Help Text")
  
    def compute_draft_burden(self):
        for rec in self:
            rec.draft_burden = 1

    def compute_approved_durden(self):
        for rec in self:
            rec.approved_burden = 1

    def compute_released_burden(self):
        for rec in self:
            rec.released_burden = 1

    def compute_closed_burden(self):
        for rec in self:
            rec.closed_burden = 1

