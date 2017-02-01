# -*- coding: utf-8 -*-
# Author: Matthieu Dietrich
# © 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api, fields


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    inventory_value = fields.Float(store=True)

    @api.multi
    @api.depends('product_id.standard_price', 'qty', 'company_id')
    def _compute_inventory_value(self):
        # Just add depends, don't redefine the function
        return super(StockQuant, self)._compute_inventory_value()
