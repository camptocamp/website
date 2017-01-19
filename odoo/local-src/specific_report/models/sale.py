# -*- coding: utf-8 -*-
# Author: Leonardo Pistone
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api, fields
import re


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_code_description = fields.Text(
        'Product code and description',
        compute='_compute_product_code_description',
    )

    @api.multi
    def _compute_product_code_description(self):
        for line in self:
            product = line.product_id
            if product:
                result = '[%s]\n%s' % (product.default_code, line.name)
            else:
                result = line.name

            line.product_code_description = result

    @api.onchange('product_id')
    def product_id_change(self):
        vals = {}
        if not self.product_id:
            return {'domain': {'product_uom': []}}
        result = super(SaleOrderLine, self).product_id_change()
        name = self.product_id.name_get()[0][1]
        if name:
            name = re.sub(r'\[.*?\] (.*)', r'\1', name)
            if self.product_id.description_sale:
                name += '\n' + self.product_id.description_sale
            vals['name'] = name
            self.update(vals)

        return result
