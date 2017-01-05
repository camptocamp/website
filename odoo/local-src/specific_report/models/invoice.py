# -*- coding: utf-8 -*-
# Author: Leonardo Pistone
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class InvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def product_id_change(self, product, uom_id, qty=0, name='',
                          type='out_invoice', partner_id=False,
                          fposition_id=False, price_unit=False,
                          currency_id=False, company_id=None):
        result = super(InvoiceLine, self).product_id_change(
            product=product,
            uom_id=uom_id,
            qty=qty,
            name=name,
            type=type,
            partner_id=partner_id,
            fposition_id=fposition_id,
            price_unit=price_unit,
            currency_id=currency_id,
            company_id=company_id,
        )

        name = result['value'] and result['value'].get('name')
        if name:
            result['value']['name'] = name.replace(u'] ', u']\n', 1)

        return result
