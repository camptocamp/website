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

This script gets the journals (account.jorunal) in an Odoo instance
and generates a CSV file to import them in Odoo 10.
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
    'currency/id',
    'loss_account_id',
    'profit_account_id',
    'type',
    'default_debit_account_id',
    'default_credit_account_id',
    'group_invoice_lines'
]

FIELDS_9_0 = [
    'id',
    'code',
    'name',
    'company_id/id',
    'currency_id/id',
    'loss_account_id',
    'profit_account_id',
    'type',
    'default_debit_account_id',
    'default_credit_account_id',
    'group_invoice_lines'
]

password = getpass.getpass()

odoo = odoorpc.ODOO(host=host, port=port)
odoo.login(db_name, user, password)

Journal = odoo.env['account.journal']
journal_ids = Journal.search([])
data = Journal.export_data(journal_ids, FIELDS)['datas']
data = [dict(zip(FIELDS_9_0, row)) for row in data]

type_mapping = {
    u'Général': 'general',
    u'Journal de situation Ouverture/Clôture': 'general',
    u'Banque et chèques': 'bank',
    u'Avoir fournisseur': 'general',
    u'Avoir de vente': 'general',
    u'Achat': 'purchase',
    u'Vente': 'sale',
}

with open(out_file, 'wb') as fo:
    writer = csv.DictWriter(fo, delimiter=',', fieldnames=FIELDS_9_0)
    writer.writeheader()
    for row in data:
        row['name'] = row['name'].encode('utf8')
        row['type'] = type_mapping[row['type']]
        if not row['currency_id/id']:
            row['currency_id/id'] = ''
        account_fields = ('loss_account_id',
                          'profit_account_id',
                          'default_debit_account_id',
                          'default_credit_account_id')
        for f in account_fields:
            if not row[f]:
                row[f] = ''
                continue
            row[f] = row[f].split()[0]  # extract account number
        row['id'] = '__setup__.journal_%s' % row['code']
        writer.writerow(row)
