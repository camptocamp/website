# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from datetime import date
from pkg_resources import resource_filename

from anthem.lyrics.records import create_or_update, add_xmlid
from anthem.lyrics.loaders import load_csv
import anthem

from openerp import fields

from ..common import req


@anthem.log
def activate_multicurrency(ctx):
    """ Activating multi-currency """
    employee_group = ctx.env.ref('base.group_user')
    employee_group.write({
        'implied_ids': [(4, ctx.env.ref('base.group_multi_currency').id)]
    })


@anthem.log
def enable_currency(ctx):
    currencies = ('GBP', 'USD', 'EUR', 'CHF')
    cc = ctx.env['res.currency'].search([('name', 'in', currencies)])
    cc.write({'active': True})


@anthem.log
def import_coa(ctx, coa):
    TaxTemplate = ctx.env['account.tax.template']
    sale_tax = TaxTemplate.search(
        [('chart_template_id', 'parent_of', coa.id),
         ('type_tax_use', '=', 'sale')], limit=1,
        order="sequence, id desc")
    purchase_tax = TaxTemplate.search(
        [('chart_template_id', 'parent_of', coa.id),
         ('type_tax_use', '=', 'purchase')], limit=1,
        order="sequence, id desc")
    wizard = ctx.env['wizard.multi.charts.accounts'].create({
        'company_id': ctx.env.user.company_id.id,
        'chart_template_id': coa.id,
        'transfer_account_id': coa.transfer_account_id.id,
        'code_digits': 8,
        'sale_tax_id': sale_tax.id,
        'purchase_tax_id': purchase_tax.id,
        'sale_tax_rate': 15,
        'purchase_tax_rate': 15,
        'complete_tax_set': coa.complete_tax_set,
        'currency_id': ctx.env.ref('base.EUR').id,
        'bank_account_code_prefix': coa.bank_account_code_prefix,
        'cash_account_code_prefix': coa.cash_account_code_prefix,
    })
    wizard.execute()


@anthem.log
def load_account(ctx):
    """ Setup CoA """
    if not ctx.env['account.account'].search([]):
        with ctx.log("Import basic CoA"):
            coa = ctx.env.ref('l10n_ch.l10nch_chart_template')
            import_coa(ctx, coa)
    with ctx.log("Import additional accounts"):
        csv_content = resource_filename(req,
                                        'data/install/account.account.csv')
        load_csv(ctx, 'account.account', csv_content)


@anthem.log
def load_banks(ctx):
    csv_content = resource_filename(req, 'data/install/res.bank.csv')
    load_csv(ctx, 'res.bank', csv_content)


@anthem.log
def load_journal(ctx):
    """ Import account.journal  """
    # add xmlids on existing journals
    mapping_codes = {
        'BNK1': 'CS',
        'CSH1': 'CASH',
    }
    for journal in ctx.env['account.journal'].search([]):
        # some journal exist in the old instance with a different code,
        # we set the same xmlid so we'll rebind them
        code = mapping_codes.get(journal.code, journal.code)
        add_xmlid(ctx, journal, '__setup__.journal_%s' % code)

    # drop extraneous journals
    ctx.env['account.journal'].search([('code', '=', 'INV')]).unlink()
    ctx.env['account.journal'].search([('code', '=', 'BILL')]).unlink()
    ctx.env['account.journal'].search([('code', '=', 'EXCH')]).unlink()

    csv_content = resource_filename(req, 'data/install/account.journal.csv')
    load_csv(ctx, 'account.journal', csv_content)


@anthem.log
def load_bank_journal(ctx):
    """ Import account.journal for banks """
    csv_content = resource_filename(req,
                                    'data/install/account.bank.journal.csv')
    load_csv(ctx, 'account.bank.journal', csv_content)


@anthem.log
def set_fiscalyear(ctx):

    type_values = {
        'name': 'Fiscal year',
        'company_id': ctx.env.ref('scenario.smartliberty_ch').id,
        'allow_overlap': False,
    }
    create_or_update(ctx, 'date.range.type',
                     '__setup__.date_range_type', type_values)

    values = {'date_start': '2016-01-01',
              'name': '2016',
              'date_end': '2016-12-31',
              'type_id': ctx.env.ref('__setup__.date_range_type').id,
              'company_id': False,
              'active': True,
              }
    create_or_update(ctx, 'date.range', '__setup__.date_range_2016', values)

    values = {'date_start': '2015-01-01',
              'name': '2015',
              'date_end': '2015-12-31',
              'type_id': ctx.env.ref('__setup__.date_range_type').id,
              'company_id': False,
              'active': True,
              }
    create_or_update(ctx, 'date.range', '__setup__.date_range_2015', values)


@anthem.log
def configure_currency_rate_live(ctx):
    """ configure enterprise module currency_rate_live """
    companies = ctx.env['res.company'].search([])

    today = date.today()
    if today.month == 12:
        next_update = today.replace(day=1, month=1, year=today.year + 1)
    else:
        next_update = today.replace(day=1, month=today.month + 1)

    companies.write({
        'currency_interval_unit': 'monthly',
        'currency_provider': 'ecb',
        'currency_next_execution_date': fields.Date.to_string(next_update)
    })


@anthem.log
def setup_invoice_sequences(ctx):
    """ Setup sequences for invoices and refund for customer and supplier """
    cp = ctx.env.user.company_id

    Journal = ctx.env['account.journal']
    journals = Journal.search([
        ('code', 'in', ('INV', 'BILL')),
        ('company_id', '=', cp.id)]
    )
    journals.write({'refund_sequence': True})
    for j in journals:
        if not j.refund_sequence_id:
            j.refund_sequence_id = j.sudo()._create_sequence(
                {'name': j.name + " Refund", 'code': j.code}, refund=True)
        if j.code == 'INV':
            j.sequence_id.prefix = 'IV'
            j.sequence_id.padding = 3
            j.refund_sequence_id.prefix = 'IV REf' + '_CN_%(year)s'
            j.refund_sequence_id.padding = 3
        else:  # BILL
            j.sequence_id.prefix = '_AP_%(year)s'
            j.sequence_id.padding = 3
            j.refund_sequence_id.prefix = '_PCN_%(year)s'
            j.refund_sequence_id.padding = 3


@anthem.log
def main(ctx):
    """ Setup accounting """
    activate_multicurrency(ctx)
    enable_currency(ctx)
    load_banks(ctx)
    set_fiscalyear(ctx)
    company_xmlid = 'scenario.smartliberty_ch'
    company = ctx.env.ref(company_xmlid)
    with ctx.log(u'Setup accounting for company %s' % company.name):
        load_account(ctx)
        load_journal(ctx)
        # load_bank_journal(ctx)
        # setup_invoice_sequences(ctx)
        configure_currency_rate_live(ctx)
