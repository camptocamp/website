# -*- coding: utf-8 -*-
#
#
#    Author: Denis Leemann
#    Copyright 2017 Camptocamp SA
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
{'name': 'Smartliberty Reports Customization',
 'summary': 'Layouts',
 'version': '10.0.1.0.0',
 'author': 'Camptocamp',
 'maintainer': 'Camptocamp',
 'category': 'Reports',
 'complexity': "normal",  # easy, normal, expert
 'depends': ['base',
             #'account',
             #'sale',
             #'sale_layout',
             #'purchase_discount',
             #'stock',
             #'delivery',
             #'mrp_repair',
             ],
 'website': 'http://www.camptocamp.com',
 'data': [
     # 'views/invoice.xml',
     'views/layouts.xml',
     # 'views/sale.xml',
     # 'views/product.xml',
     # 'views/sale_layout_template.xml',
     # 'views/templates.xml',
     # 'views/company.xml',
     # 'views/report_inventory.xml',
     # 'views/report_invoice.xml',
     # 'views/report_mrporder.xml',
     # 'views/report_picking.xml',
     # 'views/report_purchase.xml',
     # 'views/report_sale.xml',
     # 'views/report_followup.xml',
     ],
 'installable': True,
 'auto_install': False,
 'license': 'AGPL-3',
 'application': False,
 }
