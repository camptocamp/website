# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from base64 import b64encode
from pkg_resources import resource_string
import anthem

from ..common import req


@anthem.log
def setup_company(ctx):
    """ Setup company """
    company = ctx.env.ref('base.main_company')

    # load logo on company
    logo_content = resource_string(req, 'data/images/logo.png')
    b64_logo = b64encode(logo_content)
    company.logo = b64_logo

    values = {
        'name': "Smartliberty",
        'street': "",
        'zip': "",
        'city': "",
        'country_id': ctx.env.ref('base.ch').id,
        'phone': "+41 32 752 48 11",
        'fax': "+41 32 752 48 10",
        'email': "contact@smartliberty.ch",
        'website': "http://www.smartliberty.ch",
        'vat': "VAT",
        'logo': b64_logo,
        'currency_id': ctx.env.ref('base.CHF').id,
    }
    company.update(values)


@anthem.log
def setup_language(ctx):
    """ Installing language and configuring locale formatting """
    for code in ('fr_FR', 'de_DE'):
        ctx.env['base.language.install'].create({'lang': code}).lang_install()
    ctx.env['res.lang'].search([]).write({
        'grouping': [3, 0],
        'date_format': '%d/%m/%Y',
    })


@anthem.log
def set_web_base_url(ctx):
    """ Configuring web.base.url """
    url = 'http://localhost:8069'
    ctx.env['ir.config_parameter'].set_param('web.base.url', url)
    ctx.env['ir.config_parameter'].set_param('web.base.url.freeze', 'True')


@anthem.log
def main(ctx):
    """ Main: creating demo data """
    setup_company(ctx)
    setup_language(ctx)
    set_web_base_url(ctx)
