# -*- coding: utf-8 -*-
# Author: Leonardo Pistone
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class InvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def product_id_change(self):
        vals = {}
        if not self.product_id:
            return {'domain': {'product_uom': []}}
        result = super(InvoiceLine, self).product_id_change()
        name = self.product_id.with_context(
            lang=self.invoice_id.partner_id.lang).name_get()[0][1]
        if name:
            name = name.replace(u'] ', u']\n', 1)
            if self.product_id.description_sale:
                name += '\n' + self.product_id.description_sale
            vals['name'] = name
            self.update(vals)

        return result
