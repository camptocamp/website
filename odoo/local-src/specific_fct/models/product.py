# -*- coding: utf-8 -*-
# Author: Matthieu Dietrich
# © 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields

import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    volume = fields.Float(digits=dp.get_precision('Product Volume'))


class ProductProduct(models.Model):
    _inherit = 'product.product'

    volume = fields.Float(digits=dp.get_precision('Product Volume'))
