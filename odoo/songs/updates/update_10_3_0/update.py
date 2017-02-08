# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem


@anthem.log
def reload_translation(ctx, module):
    """ update translation """
    ctx.env['ir.module.module'].with_context(overwrite=True).search(
        [('name', '=', module)]).update_translations()


@anthem.log
def set_settings_proforma(ctx):
    account_config = ctx.env['account.config.settings']
    # Allow proforma invoices
    account_config.create({'group_uom': 1}).execute()


@anthem.log
def set_sales_settings(ctx):
    sale_config = ctx.env['sale.config.settings']
    # Sections in Sale lines
    sale_config.create({'group_sale_layout': 1}).execute()
    # UOM in Sale Lines
    sale_config.create({'group_uom': 1}).execute()


@anthem.log
def main(ctx):
    """ Loading data """
    # reload_translation(ctx, 'specific_report')
    set_settings_proforma(ctx)
    set_sales_settings(ctx)
