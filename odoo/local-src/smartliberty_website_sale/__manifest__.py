# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

{'name': 'Specific website sale',
 'version': '10.0.1.0.0',
 'author': 'Camptocamp SA',
 'maintainer': 'Camptocamp SA',
 'license': 'AGPL-3',
 'depends': [
     'website_sale',
     'website_menu_by_user_status',
 ],
 'website': 'www.camptocamp.com',
 'data': [
     'views/update_robots.xml',
     'data/website_menu.xml',
 ],
 'test': [],
 'installable': True,
 'auto_install': False,
 }
