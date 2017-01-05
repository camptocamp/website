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

    @api.multi
    def product_id_change(self, pricelist, product, qty=0, uom=False,
                          qty_uos=0, uos=False, name='', partner_id=False,
                          lang=False, update_tax=True, date_order=False,
                          packaging=False, fiscal_position=False, flag=False):
        result = super(SaleOrderLine, self).product_id_change(
            pricelist=pricelist,
            product=product,
            qty=qty,
            uom=uom,
            qty_uos=qty_uos,
            uos=uos,
            name=name,
            partner_id=partner_id,
            lang=lang,
            update_tax=update_tax,
            date_order=date_order,
            packaging=packaging,
            fiscal_position=fiscal_position,
            flag=flag,
        )
        name = result['value'] and result['value'].get('name')
        if name:
            result['value']['name'] = re.sub(r'\[.*?\] (.*)', r'\1', name)

        return result
