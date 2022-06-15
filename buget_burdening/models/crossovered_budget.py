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
from datetime import datetime

class Budget(models.Model):
    _inherit = 'crossovered.budget.lines'

    draft_burden = fields.Float(string='Draft Burden', help="Amount that is spent on a draft purchase order")
    approved_burden = fields.Float(string='Approved Burden', help="Amount that is spent on an approved purchase order")
    released_burden = fields.Float(string='Released Burden', help="Amount that is spent on a released purchase order")
    closed_burden = fields.Float(string='Closed Burden', help="Amount that is spent on a closed purchase order")
    total_burden = fields.Float(string='Total Burden', help="The total amount that is spent on all stages of a purchase order")
    abs_practical_amount = fields.Monetary(string='ABS Practical Amount', help="Amount really earned/spent.")
    abs_theoritical_amount = fields.Monetary(string='ABS Theoretical Amount',  help="Amount you are supposed to have earned/spent at this date.")
    abs_planned_amount = fields.Monetary(string='ABS Planned Amount', help="Amount you plan to earn/spend. Record a positive amount if it is a revenue and a negative amount if it is a cost.")


