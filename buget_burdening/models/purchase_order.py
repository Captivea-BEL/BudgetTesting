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

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
    ('draft', 'Draft PO'),
    ('sent', 'Draft PO Sent'),
    ('to approve', 'To Approve'),
    ('to reapprove', 'To Reapprove'),
    ('approved', 'Approved'),
    ('purchase', 'Released'),
    ('cancel', 'Cancelled'),
    ('revised', 'Revised'),
    ('done', 'Locked'),
    ('closed', 'Closed'),
    
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order.line'

    date_promised = fields.Date(string='Promise Date', required=True, copy=True)

    @api.onchange('date_promised','price_total','account_analytic_id')
    def onchange_budget_burden(self):
        if self.date_promised and self.price_total and self.account_analytic_id:
            min_time = datetime.min.time()
            po_date = datetime.combine(self.date_promised, min_time)
            budget = self.env['crossovered.budget.lines'].search([
                ('analytic_account_id','=', self.analytic_account_id.id),
                ('date_from', '>=', po_date ),
                ('date_to', '<=', po_date )
            ])
            if budget:
                po_lines = self.env['purchase.order.line'].search([
                    ('account_analytic_id','=', budget.analytic_account_id.id),                    
                    ('date_promised', '>=', budget.date_from ),
                    ('date_promised', '<=', budget.date_to )
                ])
                budget.draft_burden = self.sum_lines(po_lines.filtered(lambda line: line.order_id.state in ['draft','sent','to approve', 'to reapprove']))
                budget.approved_burden = self.sum_lines(po_lines.filtered(lambda line: line.order_id.state in ['approved']))
                budget.released_burden = po_lines.filtered(lambda line: line.order_id.state in ['purchase'])
                budget.closed_burden = po_lines.filtered(lambda line: line.order_id.state in ['done', 'closed'])
                budget.abs_theoritical_amount = abs(budget.abs_theoritical_amount)
                budget.abs_practical_amount = abs(budget.abs_practical_amount)
                budget.abs_planned_amount = abs(budget.abs_planned_amount)
                
                
                budget.total_burden = budget.draft_burden + budget.approved_burden + budget.released_burden + budget.closed_burden + budget.practical

    def sum_lines(po_lines):
        total_burden = 0.0
        for po_line in po_lines:
            if po_line.product_qty != 0:
                units = (po_line.product_qty - po_line.qty_invoiced)
                total_burden += po_line.price_unit * units
        return total_burden









