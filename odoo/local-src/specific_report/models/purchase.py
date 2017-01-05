# -*- coding: utf-8 -*-
# Author: Leonardo Pistone
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class PurchaseLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.multi
    def onchange_product_id(self, pricelist_id, product_id, qty, uom_id,
                            partner_id, date_order=False,
                            fiscal_position_id=False, date_planned=False,
                            name=False, price_unit=False, state='draft'):
        result = super(PurchaseLine, self).onchange_product_id(
            pricelist_id,
            product_id,
            qty,
            uom_id,
            partner_id,
            date_order,
            fiscal_position_id,
            date_planned,
            name,
            price_unit,
            state,
        )

        name = result['value'] and result['value'].get('name')
        if name:
            result['value']['name'] = name.replace(u'] ', u']\n', 1)

        return result
