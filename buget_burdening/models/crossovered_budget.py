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

    draft_burden = fields.Float(string='Draft Burden', compute="compute_draft_burden",
                                 help="Amount that is spent on a draft purchase order")
    approved_burden = fields.Float(string='Approved Burden', compute="compute_approved_durden",
                                  help="Amount that is spent on an approved purchase order")
    released_burden = fields.Float(string='Released Burden', compute="compute_released_burden",
                                  help="Amount that is spent on a released purchase order")
    closed_burden = fields.Float(string='Closed Burden', compute="compute_closed_burden",
                                  help="Amount that is spent on a closed purchase order")
    total_burden = fields.Float(string='Total Burden', compute="compute_total_burden",
                                  help="The total amount that is spent on all stages of a purchase order")
    abs_practical_amount = fields.Monetary(string='ABS Practical Amount', compute='_compute_abs_practical_amount',
                                    help="Amount really earned/spent.")
    abs_theoritical_amount = fields.Monetary(string='ABS Theoretical Amount', compute='_compute_abs_theoritical_amount',
                                    help="Amount you are supposed to have earned/spent at this date.")
    abs_planned_amount = fields.Monetary(string='ABS Planned Amount', compute='_compute_abs_planned_amount',
                                    help="Amount you plan to earn/spend. Record a positive amount if it is a revenue and a negative amount if it is a cost.")



    def compute_draft_burden(self):
        for rec in self: 
            start_time = datetime.min.time()
            start_date = datetime.combine(rec.date_from, start_time)
            end_time = datetime.max.time()
            end_date = datetime.combine(rec.date_to, end_time)         
            po_lines = self.env['purchase.order.line'].search([
                ('account_analytic_id','=', rec.analytic_account_id.id),
                ('order_id.state','in', ['draft','sent','to approve', 'to reapprove']),
                ('date_promised', '>=', start_date ),
                ('date_promised', '<=', end_date )
            ])
            total_burden = 0.0
            for po_line in po_lines:
                if po_line.product_qty != 0:
                    units = (po_line.product_qty - po_line.qty_invoiced)
                    total_burden += po_line.price_unit * units
            rec.draft_burden = total_burden

    def compute_approved_durden(self):
        for rec in self: 
            start_time = datetime.min.time()
            start_date = datetime.combine(rec.date_from, start_time)
            end_time = datetime.max.time()
            end_date = datetime.combine(rec.date_to, end_time)         
            po_lines = self.env['purchase.order.line'].search([
                ('account_analytic_id','=', rec.analytic_account_id.id),
                ('order_id.state','in', ['approved']),
                ('date_promised', '>=', start_date ),
                ('date_promised', '<=', end_date )
            ])
            total_burden = 0.0
            for po_line in po_lines:
                if po_line.product_qty != 0:
                    units = (po_line.product_qty - po_line.qty_invoiced)
                    total_burden += po_line.price_unit * units
            rec.approved_burden = total_burden

    def compute_released_burden(self):
        for rec in self: 
            start_time = datetime.min.time()
            start_date = datetime.combine(rec.date_from, start_time)
            end_time = datetime.max.time()
            end_date = datetime.combine(rec.date_to, end_time)         
            po_lines = self.env['purchase.order.line'].search([
                ('account_analytic_id','=', rec.analytic_account_id.id),
                ('order_id.state','in', ['purchase']),
                ('date_promised', '>=', start_date ),
                ('date_promised', '<=', end_date )
            ])
            total_burden = 0.0
            for po_line in po_lines:
                if po_line.product_qty != 0:
                    units = (po_line.product_qty - po_line.qty_invoiced)
                    total_burden += po_line.price_unit * units
            rec.released_burden = total_burden

    def compute_closed_burden(self):
        for rec in self: 
            start_time = datetime.min.time()
            start_date = datetime.combine(rec.date_from, start_time)
            end_time = datetime.max.time()
            end_date = datetime.combine(rec.date_to, end_time)         
            po_lines = self.env['purchase.order.line'].search([
                ('account_analytic_id','=', rec.analytic_account_id.id),
                ('order_id.state','in', ['done', 'closed']),
                ('date_promised', '>=', start_date ),
                ('date_promised', '<=', end_date )
            ])
            total_burden = 0.0
            for po_line in po_lines:
                if po_line.product_qty != 0:
                    units = (po_line.product_qty - po_line.qty_invoiced)
                    total_burden += po_line.price_unit * units
            rec.closed_burden = total_burden
    
    def compute_total_burden(self):
        for rec in self: 
            amounts = [rec.practical_amount, rec.released_burden, rec.approved_burden, rec.draft_burden, rec.closed_burden]
            total = 0
            for amount in amounts:
                total += abs(amount)
            rec.total_burden = total


    @api.depends('theoritical_amount')
    def _compute_abs_theoritical_amount(self):
        for rec in self:
            rec.abs_theoritical_amount = abs(rec.theoritical_amount)
            
    @api.depends('practical_amount')
    def _compute_abs_practical_amount(self):
        for rec in self:
            rec.abs_practical_amount = abs(rec.practical_amount)

    @api.depends('planned_amount')
    def _compute_abs_planned_amount(self):
        for rec in self:
            rec.abs_planned_amount = abs(rec.planned_amount)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):        
        fields_list = {
            'practical_amount', 
            'draft_burden', 
            'approved_burden', 
            'released_burden', 
            'closed_burden', 
            'total_burden', 
            'theoritical_amount', 
            'percentage'}

        def truncate_aggr(field):
            field_no_aggr = field.split(':', 1)[0]
            if field_no_aggr in fields_list:
                return field_no_aggr
            return field
        fields = {truncate_aggr(field) for field in fields}

        result = super(Budget, self).read_group(domain, list(fields - fields_list), groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)

        if fields & fields_list:
            for group_line in result:
                if 'abs_planned_amount' in fields:
                    group_line['abs_planned_amount'] = 0
                if 'abs_practical_amount' in fields:
                    group_line['abs_practical_amount'] = 0
                if 'draft_burden' in fields:
                    group_line['draft_burden'] = 0
                if 'approved_burden' in fields:
                    group_line['approved_burden'] = 0
                if 'released_burden' in fields:
                    group_line['released_burden'] = 0
                if 'closed_burden' in fields:
                    group_line['closed_burden'] = 0
                if 'total_burden' in fields:
                    group_line['total_burden'] = 0
                if 'abs_theoritical_amount' in fields:
                    group_line['abs_theoritical_amount'] = 0
                if 'percentage' in fields:
                    group_line['percentage'] = 0
                    group_line['abs_practical_amount'] = 0
                    group_line['abs_theoritical_amount'] = 0

                domain = group_line.get('__domain') or domain
                all_budget_lines_that_compose_group = self.search(domain)

                for budget_line_of_group in all_budget_lines_that_compose_group:
                    if 'abs_planned_amount' in fields or 'percentage' in fields:
                        group_line['abs_planned_amount'] += budget_line_of_group.abs_planned_amount
                    if 'abs_practical_amount' in fields or 'percentage' in fields:
                        group_line['abs_practical_amount'] += budget_line_of_group.abs_practical_amount
                    if 'draft_burden' in fields or 'percentage' in fields:
                        group_line['draft_burden'] += budget_line_of_group.draft_burden
                    if 'approved_burden' in fields or 'percentage' in fields:
                        group_line['approved_burden'] += budget_line_of_group.approved_burden
                    if 'released_burden' in fields or 'percentage' in fields:
                        group_line['released_burden'] += budget_line_of_group.released_burden
                    if 'closed_burden' in fields or 'percentage' in fields:
                        group_line['closed_burden'] += budget_line_of_group.closed_burden
                    if 'total_burden' in fields or 'percentage' in fields:
                        group_line['total_burden'] += budget_line_of_group.total_burden
                    if 'abs_theoritical_amount' in fields or 'percentage' in fields:
                        group_line['abs_theoritical_amount'] += budget_line_of_group.abs_theoritical_amount
                    if 'percentage' in fields:
                        if group_line['abs_theoritical_amount']:
                            group_line['percentage'] = float(
                                (group_line['abs_practical_amount'] or 0.0) / group_line['abs_theoritical_amount'])
        return result       