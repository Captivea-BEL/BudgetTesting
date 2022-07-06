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

    def write(self, vals):
        vals, partner_vals = self._write_partner_values(vals)
        res = super().write(vals)
        if partner_vals:
            self.partner_id.sudo().write(partner_vals)  
        ####################################
        self.env['purchase.order.line'].set_burden_vals(self.order_line)
        ###################################
        return res
    
    @api.model
    def create(self, vals):
        company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
        self_comp = self.with_company(company_id)
        if vals.get('name', 'New') == 'New':
            seq_date = None
            if 'date_order' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
            vals['name'] = self_comp.env['ir.sequence'].next_by_code('purchase.order', sequence_date=seq_date) or '/'
        vals, partner_vals = self._write_partner_values(vals)
        res = super(PurchaseOrder, self_comp).create(vals)
        ###################################
        self.env['purchase.order.line'].set_burden_vals(res.order_line)
        ###################################
        if partner_vals:
            res.sudo().write(partner_vals) 
        return res

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    date_promised = fields.Date(string='Promise Date', required=True, copy=True)
    
    def set_burden_vals(self, input_lines):
        for line in input_lines:
            budgets = self.env['crossovered.budget.lines'].search([
                ('analytic_account_id','=', line.account_analytic_id.id)
                ])
            for budget in budgets:
                po_lines = self.env['purchase.order.line'].search([
                    ('account_analytic_id.id','=', budget.analytic_account_id.id),                    
                    ('date_promised', '>=', budget.date_from ),
                    ('date_promised', '<=', budget.date_to )
                ])
                draft = 0
                approved = 0
                released = 0
                closed = 0
                total = 0

                for po_line in po_lines:
                    amount = 0
                    if po_line.product_qty != 0:
                        units = (po_line.product_qty - po_line.qty_invoiced)
                        amount = po_line.price_unit * units
                    total += amount
                    if po_line.order_id.state in ['draft','sent','to approve', 'to reapprove']:
                        draft += amount
                    if po_line.order_id.state in ['approved']:
                        approved += amount
                    if po_line.order_id.state in ['done', 'closed']:
                        closed += amount
                    if po_line.order_id.state in ['purchase']:
                        released += amount
                _logger.info('draftt is ' + str(draft) + " budget is " + budget.name + " date from is " + str(budget.date_from))
                budget.draft_burden = draft
                budget.approved_burden = approved
                budget.closed_burden = closed
                budget.released_burden = released
                budget.total_burden = total 