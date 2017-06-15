# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA (Nicolas Bessi)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrderMerge(models.TransientModel):
    """Wizard that merges draft sale orders into a given draf sale order.
    A sale order can be merged in a target sale order if:
        - Sales order is in a draft state
        - Sales order have the same customer and addresses
          as current sales orders
        - Sales order is from the same company
        - Sales order is not related to any invoices or picking
    """

    _name = "draft_sale_order_merger"

    @api.multi
    def _get_active_id(self):
        """Boiler plate that check environement for active_id"""
        active_id = self.env.context.get('active_id')
        if not active_id:
            raise ValueError('No target SO active id given')
        return active_id

    @api.multi
    def _get_target(self):
        """Set the target sales order
        :return: the target sales order id
        """
        return self._get_active_id()

    @api.multi
    def _get_candidates(self):
        """Retrieve sales order that can potentially be merged in target.
        For more details see sale.order _compute_eligible_merge_candidates
        :returns: a recordset of sales order
        """
        active_id = self._get_active_id()
        target = self.env['sale.order'].browse(active_id)
        return target.merge_candidates

    def _get_target_state(self):
        """Return target sales order state.
        Related field can not be used
        as source state is of type selection
        """
        active_id = self._get_active_id()
        target = self.env['sale.order'].browse(active_id)
        return target.state

    merge_candidates = fields.Many2many(
        'sale.order',
        'draft_so_merg_rel',
        'merger_id',
        'sale_order_id',
        default=_get_candidates,
        string='Sales order to merge',
        help=('Choose the sales order you want to merge into '
              'the main one'),
        Copy=False,
    )

    target_so = fields.Many2one(
        'sale.order',
        string='Target Sales order',
        help='All selected Sales order will be merged into this one',
        default=_get_target,
        readonly=True,
        required=True,
    )

    target_state = fields.Char(
        string='Target sales order state',
        default=_get_target_state,
        store=False
    )

    def merge_sale_orders(self):
        """Merge candidates sales order into target sales order.
        The sales order lines of candidate are copied in the target.
        Then the candidate is deactivated. This allows to retrive
        source sales order in case of problem. We do not copy target
        sales order to keep history and sales stats.
        """
        target = self.target_so
        target.ensure_valid_merge_target()
        valid_candidates = target.merge_candidates
        for candidate in valid_candidates:
            if candidate not in valid_candidates:
                raise UserError(
                    _('Sales order %s can not be merged inte '
                      'Sales order %s') % (candidate.name, target.name))
            self.copy_so_lines_to_target(candidate, target)
            candidate.write({'active': False})
            self.log_action(valid_candidates, target)

    def copy_so_lines_to_target(self, candidate, target):
        """Copy sales order lines on target sales order
        :param candidate: of candidate sales order record
        :param target: the target sales order
        """
        for so_line in candidate.order_line:
            so_line.copy({'order_id': target.id})

    def log_action(self, candidates, target):
        """Logs merge history into target wall.
        :param candidates: Recordset of candidate sales order.
        :param target: the target sales order record
        """
        message = _("Following sales orders are merged into %s: \n\n %s") % (
            target.name,
            "\n".join("    - {}".format(so.name) for so in candidates)
        )
        target.message_post(body=message, content_subtype='plaintext')
