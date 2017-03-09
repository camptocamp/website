# -*- coding: utf-8 -*-
# Author: Matthieu Dietrich
# © 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_uom_qty', 'product_uom', 'route_id')
    def _onchange_product_id_check_availability(self):
        ret_val = super(
            SaleOrderLine, self)._onchange_product_id_check_availability()
        if 'warning' in ret_val:
            ret_val.pop('warning', None)
        return ret_val
