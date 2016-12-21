#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import csv
import sys
import getpass

import odoorpc

USAGE = """{} user@host:port db_name out_file

host\t\tOdoo instance to get the data (e.g. localhost:8069)
db_name\t\todoo db name
out_file\tdestination file

This script gets the new accounts (account.account) in an Odoo instance
and generates a CSV file to import them in Odoo 10.
To find the new accouts, it compares the account.account table and
account.account.template table.
""".format(sys.argv[0])

if not len(sys.argv) == 4:
    print(USAGE)
    sys.exit(1)

host = sys.argv[1]
db_name = sys.argv[2]
out_file = sys.argv[3]

try:
    host, port = host.split(':')
    user, host = host.split('@')
except ValueError:
    print('host format must be "host:port"')
    sys.exit(1)

FIELDS = [
    'id',
    'code',
    'name',
    'company_id/id',
    'currency_id/id',
    'reconcile',
    'user_type/id',
]

FIELDS_9_0 = [
    'id',
    'code',
    'name',
    'company_id/id',
    'currency_id/id',
    'reconcile',
    'user_type_id/id',
]

password = getpass.getpass()

odoo = odoorpc.ODOO(host=host, port=port)
odoo.login(db_name, user, password)

MoveLine = odoo.env['account.move.line']
Account = odoo.env['account.account']
domain = [
    ('type', '!=', 'view'),
]
account_ids = Account.search(domain)
account_ids = [id_ for id_ in account_ids
               if MoveLine.search([('account_id', '=', id_)], limit=1)]

data = Account.export_data(account_ids, FIELDS)['datas']
data = [dict(zip(FIELDS_9_0, row)) for row in data]

user_type_mapping = {
    'account.data_account_type_cash': 'account.data_account_type_liquidity',
    'account.data_account_type_bank': 'account.data_account_type_liquidity',
    'l10n_ch.account_type_inventory': \
            'account.data_account_type_current_assets',
    'l10n_ch.account_type_intangible_asset': \
            'account.data_account_type_fixed_assets',
    'account.data_account_type_asset': \
            'account.data_account_type_current_assets',
    'account.data_account_type_liability': \
            'account.data_account_type_current_liabilities',
    'l10n_ch.account_type_income': 'account.data_account_type_revenue',
    'l10n_ch.account_type_purchase': 'account.data_account_type_expenses',
    'l10n_ch.account_type_personnal_exp': 'account.data_account_type_expenses',
    'l10n_ch.account_type_other_ope_exp': 'account.data_account_type_expenses',
    'l10n_ch.account_type_depreciation': \
            'account.data_account_type_depreciation',
    'l10n_ch.account_type_non_ope_result': \
            'account.data_account_type_other_income',
    'l10n_ch.account_type_report_result': \
            'account.data_account_type_other_income',
    'l10n_ch.account_type_adj_liability': \
            'account.data_account_type_current_liabilities',
    'l10n_ch.account_type_adjusting_asset': \
            'account.data_account_type_current_assets',
    'l10n_ch.account_type_cash': \
            'account.data_account_type_current_assets',
    'l10n_ch.account_type_equity': \
            'account.data_account_type_equity',
    'l10n_ch.account_type_financial_result': \
            'account.data_account_type_expenses',
    'l10n_ch.account_type_fixed_asset': \
            'account.data_account_type_current_assets',
    'l10n_ch.account_type_other_receivable': \
        'account.data_account_type_current_assets',
    'l10n_ch.account_type_payable': \
        'account.data_account_type_payable',
    'l10n_ch.account_type_prov_reserve': \
        'account.data_account_type_equity',
    'l10n_ch.account_type_receivable': \
        'account.data_account_type_receivable',
    # TODO: check
    'l10n_ch.account_type_closing': 'account.data_unaffected_earnings',
    'l10n_ch.account_type_financial_asset': \
            'account.data_account_type_current_assets',

}

reconcilable = ('account.data_account_type_payable',
                'account.data_account_type_receivable')
errors = {}
with open(out_file, 'wb') as fo:
    writer = csv.DictWriter(fo, delimiter=',', fieldnames=FIELDS_9_0)
    writer.writeheader()
    for row in data:
        row['id'] = '__setup__.account_%s' % row['code'].replace('.', '_')
        row['name'] = row['name'].encode('utf8')
        row['user_type_id/id'] = user_type_mapping[row['user_type_id/id']]
        if not row['currency_id/id']:
            row['currency_id/id'] = ''
        if row['user_type_id/id'] in reconcilable:
            row['reconcile'] = 'True'
        writer.writerow(row)
