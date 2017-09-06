# -*- coding: utf-8 -*-
#
#
#    Author: Leonardo Pistone, Denis Leemann
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
{'name': 'Smartliberty Specific Customisation',
 'summary': 'Layouts',
 'version': '10.0.1.0.0',
 'author': 'Camptocamp',
 'maintainer': 'Camptocamp',
 'category': 'Reports',
 'depends': ['stock',
             'product',
             'sale_stock',
             'base',
             'website_event_sale',
             ],
 'website': 'http://www.camptocamp.com',
 'data': ['views/stock.xml',
          'views/partner.xml',
          'views/website_event.xml',
          'data/product_data.xml',
          ],
 'installable': True,
 'auto_install': False,
 'license': 'AGPL-3',
 'application': False,
 }
