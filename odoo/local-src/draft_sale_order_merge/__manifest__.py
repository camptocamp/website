# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA (Nicolas Bessi)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{'name': 'Draft sale order merge',
 'summary': 'Merge draft sales orders',
 'version': '0.1',
 'author': 'Camptocamp',
 'maintainer': 'Camptocamp',
 'category': 'Sales',
 'complexity': 'easy',
 'depends': ['sale', 'sale_stock'],
 'description': """
Merge draft sales orders
========================

Merge draft sales order under following constraints:
- Sales order is in a draft state
- Sales order have the same customer and addresses
- Sales order are from the same company
- Sales order are not related to any invoices

The merge is called from the origin sales order.

When merging, data will be taken from original sales order
- dates
- price list
- payment terms
- etc.

The SO lines will not be merged.
The action is not destructive the merged on merged SO.
They are deactivated and renamed.
Target SO will have his lines altered directly in order
to preserve numeration and references.
""",
 'website': 'http://www.camptocamp.com',
 'data': ['wizard/sale_order_merge.xml',
          'views/inherited_sale.xml',
          'security/ir.model.access.csv'],
 'demo': [],
 'test': [],
 'auto_install': False,
 'active': True,
 'installable': True,
 'license': 'AGPL-3',
 'application': False,
 }
