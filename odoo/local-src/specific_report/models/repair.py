# -*- coding: utf-8 -*-
# Author: Matthieu Dietrich
# © 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class MrpRepair(models.Model):
    _inherit = 'mrp.repair'

    analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic Account'
    )
