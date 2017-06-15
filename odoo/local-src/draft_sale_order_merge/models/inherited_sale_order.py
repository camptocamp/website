# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA (Nicolas Bessi)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    """Inherit "sale.order" model to add relations to merge.
   We put this knowledge here to allow the development of a search
   and filter on those fields."""

    _inherit = "sale.order"

    active = fields.Boolean(
        default=True,
        help=('If the active field is set to false, '
              'it will allow you to hide the Sales order without removing it'))

    merge_candidates = fields.Many2many(
        comodel_name='sale.order',
        compute='_compute_eligible_merge_candidates')

    @api.multi
    def _compute_eligible_merge_candidates(self):
        """Determine candidates for given sales order.
        A candidate is eligible if:
        - Sales order is in a draft state
        - Sales order have the same customer and addresses
          as current sales orders
        - Sales order is from the same company
        - Sales order is not related to any invoices or picking
        :return: Sale order recordset of SO that can be merged
        """
        for so in self:
            so.merge_candidates = self.search(
                so.compute_eligible_mere_candidate_domain()
            )

    def compute_eligible_mere_candidate_domain(self):
        """compute eligible candidate domain
        A candidate is eligible if:

        - Sales order is in a draft state
        - Sales order have the same customer and addresses
          as current sales orders
        - Sales order is from the same company
        - Sales order is not related to any invoices or picking
        """
        domain = [
            ('id', '!=', self.id),
            ('partner_id', '=', self.partner_id.id),
            ('partner_shipping_id', '=', self.partner_shipping_id.id),
            ('partner_invoice_id', '=', self.partner_invoice_id.id),
            ('warehouse_id', '=', self.warehouse_id.id),
            ('company_id', '=', self.company_id.id),
            ('state', '=', 'draft'),
            ('invoice_ids', '=', False),
            ('picking_ids', '=', False),
        ]
        return domain

    def ensure_valid_merge_target(self):
        """Ensure that a potential merge target meets requierments.
        The target must be in draft state and must not be related
        to any invoice or delivery
        """
        if any([self.invoice_ids, self.picking_ids]):
            raise UserError(
                _('Sales order %s is related to invoice or delivery') % self.name
            )
        if self.state != 'draft':
            raise UserError(
                _('Sales order %s is not a quotation') % self.name
            )
        return True
