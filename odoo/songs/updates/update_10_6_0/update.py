# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)


import anthem


@anthem.log
def set_web_m2x_options_settings(ctx):
    """ Add settings """
    ir_config_parameter = ctx.env['ir.config_parameter']
    # Remove quick create from all model
    web_m2x_options_create = ir_config_parameter.search(
        [('key', '=', 'web_m2x_options.create')]
    )
    if web_m2x_options_create:
        ir_config_parameter.write({'value': 'False'})
    else:
        ir_config_parameter.create({'key': 'web_m2x_options.create',
                                    'value': 'False'})


@anthem.log
def main(ctx):
    """ Loading data """
    set_web_m2x_options_settings(ctx)
