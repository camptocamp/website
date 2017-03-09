# -*- coding: utf-8 -*-
# Author: Matthieu Dietrich
# © 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api, fields
from odoo.tools.float_utils import float_round


class StockMove(models.Model):
    _inherit = 'stock.move'

    delivered_qty = fields.Float(
        'Delivered Quantity', compute='_get_delivered_qty',
        digits=0, readonly=True)

    @api.multi
    @api.depends('linked_move_operation_ids.qty')
    def _get_delivered_qty(self):
        for move in self:
            move.delivered_qty = float_round(
                sum(
                    move.mapped(
                        'linked_move_operation_ids.operation_id.qty_done'
                    )
                ),
                precision_rounding=move.product_id.uom_id.rounding)
