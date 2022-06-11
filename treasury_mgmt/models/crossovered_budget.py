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
                                 help="TODO Help Text")
    approved_burden = fields.Float(string='Approved Burden', compute="compute_approved_durden",
                                  help="TODO Help Text")
    released_burden = fields.Float(string='Released Burden', compute="compute_released_burden",
                                  help="TODO Help Text")
    closed_burden = fields.Float(string='closed Burden', compute="compute_closed_burden",
                                  help="TODO Help Text")
  
    def compute_draft_burden(self):
        for rec in self: 
            start_time = datetime.min.time()
            start_date = datetime.combine(rec.date_from, start_time)
            end_time = datetime.max.time()
            end_date = datetime.combine(rec.date_to, end_time)         
            po_lines = self.env['purchase.order.line'].search([
                ('account_analytic_id','=', rec.analytic_account_id.id),
                ('order_id.state','in', ['draft','sent','to approve']),
                ('order_id.date_approve', '>=', start_date ),
                ('order_id.date_approve', '<=', end_date )
            ])
            total_burden = 0.0
            for po_line in po_lines:
                if po_line.product_qty != 0:
                    units = (po_line.product_qty - po_line.qty_invoiced)
                    tax = po_line.price_tax/po_line.product_qty * units
                    subtotal = po_line.price_unit * units
                    total_burden += tax + subtotal
            rec.draft_burden = total_burden

    def compute_approved_durden(self):
        for rec in self: 
            start_time = datetime.min.time()
            start_date = datetime.combine(rec.date_from, start_time)
            end_time = datetime.max.time()
            end_date = datetime.combine(rec.date_to, end_time)         
            po_lines = self.env['purchase.order.line'].search([
                ('account_analytic_id','=', rec.analytic_account_id.id),
                ('order_id.state','in', ['purchase']),
                ('order_id.date_approve', '>=', start_date ),
                ('order_id.date_approve', '<=', end_date )
            ])
            total_burden = 0.0
            for po_line in po_lines:
                if po_line.product_qty != 0:
                    units = (po_line.product_qty - po_line.qty_invoiced)
                    tax = po_line.price_tax/po_line.product_qty * units
                    subtotal = po_line.price_unit * units
                    total_burden += tax + subtotal
            rec.approved_burden = total_burden

    def compute_released_burden(self):
        for rec in self: 
            start_time = datetime.min.time()
            start_date = datetime.combine(rec.date_from, start_time)
            end_time = datetime.max.time()
            end_date = datetime.combine(rec.date_to, end_time)         
            po_lines = self.env['purchase.order.line'].search([
                ('account_analytic_id','=', rec.analytic_account_id.id),
                ('order_id.state','in', ['released']),
                ('order_id.date_approve', '>=', start_date ),
                ('order_id.date_approve', '<=', end_date )
            ])
            total_burden = 0.0
            for po_line in po_lines:
                if po_line.product_qty != 0:
                    units = (po_line.product_qty - po_line.qty_invoiced)
                    tax = po_line.price_tax/po_line.product_qty * units
                    subtotal = po_line.price_unit * units
                    total_burden += tax + subtotal
            rec.released_burden = total_burden

    def compute_closed_burden(self):
        for rec in self: 
            start_time = datetime.min.time()
            start_date = datetime.combine(rec.date_from, start_time)
            end_time = datetime.max.time()
            end_date = datetime.combine(rec.date_to, end_time)         
            po_lines = self.env['purchase.order.line'].search([
                ('account_analytic_id','=', rec.analytic_account_id.id),
                ('order_id.state','in', ['done']),
                ('order_id.date_approve', '>=', start_date ),
                ('order_id.date_approve', '<=', end_date )
            ])
            total_burden = 0.0
            for po_line in po_lines:
                if po_line.product_qty != 0:
                    units = (po_line.product_qty - po_line.qty_invoiced)
                    tax = po_line.price_tax/po_line.product_qty * units
                    subtotal = po_line.price_unit * units
                    total_burden += tax + subtotal
            rec.closed_burden = total_burden

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        # overrides the default read_group in order to compute the computed fields manually for the group
        fields_list = {
            'practical_amount', 
            'draft_burden', 
            'approved_burden', 
            'released_burden', 
            'closed_burden', 
            'theoritical_amount', 
            'percentage'}

        # Not any of the fields_list support aggregate function like :sum
        def truncate_aggr(field):
            field_no_aggr = field.split(':', 1)[0]
            if field_no_aggr in fields_list:
                return field_no_aggr
            return field
        fields = {truncate_aggr(field) for field in fields}

        # Read non fields_list fields
        result = super(Budget, self).read_group(domain, list(fields - fields_list), groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)

        # Populate result with fields_list values
        if fields & fields_list:
            for group_line in result:

                # initialise fields to compute to 0 if they are requested
                if 'practical_amount' in fields:
                    group_line['practical_amount'] = 0
                if 'draft_burden' in fields:
                    group_line['draft_burden'] = 0
                if 'approved_burden' in fields:
                    group_line['approved_burden'] = 0
                if 'released_burden' in fields:
                    group_line['released_burden'] = 0
                if 'closed_burden' in fields:
                    group_line['closed_burden'] = 0
                if 'theoritical_amount' in fields:
                    group_line['theoritical_amount'] = 0
                if 'percentage' in fields:
                    group_line['percentage'] = 0
                    group_line['practical_amount'] = 0
                    group_line['theoritical_amount'] = 0

                domain = group_line.get('__domain') or domain
                all_budget_lines_that_compose_group = self.search(domain)

                for budget_line_of_group in all_budget_lines_that_compose_group:
                    if 'practical_amount' in fields or 'percentage' in fields:
                        group_line['practical_amount'] += budget_line_of_group.practical_amount
                    if 'draft_burden' in fields or 'percentage' in fields:
                        group_line['draft_burden'] += budget_line_of_group.draft_burden
                    if 'approved_burden' in fields or 'percentage' in fields:
                        group_line['approved_burden'] += budget_line_of_group.approved_burden
                    if 'released_burden' in fields or 'percentage' in fields:
                        group_line['released_burden'] += budget_line_of_group.released_burden
                    if 'closed_burden' in fields or 'percentage' in fields:
                        group_line['closed_burden'] += budget_line_of_group.closed_burden
                    if 'theoritical_amount' in fields or 'percentage' in fields:
                        group_line['theoritical_amount'] += budget_line_of_group.theoritical_amount
                    if 'percentage' in fields:
                        if group_line['theoritical_amount']:
                            # use a weighted average
                            group_line['percentage'] = float(
                                (group_line['practical_amount'] or 0.0) / group_line['theoritical_amount'])
        return result       