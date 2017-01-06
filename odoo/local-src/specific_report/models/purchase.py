# -*- coding: utf-8 -*-
# Author: Leonardo Pistone
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class PurchaseLine(models.Model):
    _inherit = 'purchase.order.line'

    @api.onchange('product_id')
    def onchange_product_id(self):
        result = {}
        if not self.product_id:
            return result

        result = super(PurchaseLine, self).onchange_product_id()

        product_lang = self.product_id.with_context({
            'lang': self.partner_id.lang,
            'partner_id': self.partner_id.id,
        })
        self.name = product_lang.display_name
        if self.name:
            if product_lang.description_purchase:
                self.name += '\n' + product_lang.description_purchase
            self.name = self.name.replace(u'] ', u']\n', 1)

        return result
