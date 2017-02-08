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
def update_lang_format(ctx):
    langs = ['base.lang_fr', 'base.lang_de', 'base.lang_en']
    vals = {
        'thousands_sep': "'",
        'grouping': '[3,0]',
        'decimal_point': '.',
        'date_format': '%d. %m. %Y',
        'time_format': '%H:%M:%S',
    }
    for lang in langs:
        res_lang = ctx.env.ref(lang)
        res_lang.write(vals)


@anthem.log
def update_bvr_layout_settings(ctx):
    company = ctx.env.ref('base.main_company')
    vals = {
        'bvr_add_horz': '0.15',
        'bvr_add_vert': '-0.25',
        'bvr_background': False,
        'bvr_delta_horz': '0.00',
        'bvr_delta_vert': '0.00',
        'bvr_scan_line_front_size': '0',
        'bvr_san_line_horz': '-0.04',
        'bvr_san_letter_spacing': '0.00',
        'bvr_san_line_vert': '0.04',
        'merge_mode': 'in_memory'
    }
    company.write(vals)


@anthem.log
def main(ctx):
    """ Loading data """
    # reload_translation(ctx, 'specific_report')
    set_settings_proforma(ctx)
    set_sales_settings(ctx)
    update_lang_format(ctx)
    update_bvr_layout_settings(ctx)
