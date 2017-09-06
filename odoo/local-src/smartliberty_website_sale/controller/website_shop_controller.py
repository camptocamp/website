# -*- coding: utf-8 -*-
# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import http
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):
    ''' Override shop routes to enforce authentication '''

    @http.route(auth="user")
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        ''' Set authentication for sale '''
        return super(WebsiteSale, self).shop(
            page=page, category=category, search=search, ppg=ppg, **post)

    @http.route(auth="user")
    def product(self, product, category='', search='', **kwargs):
        return super(WebsiteSale, self).product(
            product=product, category=category, search=search, **kwargs)

    @http.route(auth="user")
    def pricelist_change(self, pl_id, **post):
        return super(WebsiteSale, self).pricelist_change(
            pl_id=pl_id, **post)

    @http.route(auth="user")
    def pricelist(self, promo, **post):
        return super(WebsiteSale, self).pricelist(promo=promo, **post)

    @http.route(auth="user")
    def cart(self, **post):
        return super(WebsiteSale, self).cart(**post)

    @http.route(auth="user")
    def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
        return super(WebsiteSale, self).cart_update(
            product_id=product_id, add_qty=add_qty, set_qty=set_qty, **kw)

    @http.route(auth="user")
    def cart_update_json(self, product_id, line_id=None, add_qty=None,
                         set_qty=None, display=True):
        return super(WebsiteSale, self).cart_update_json(
            product_id=product_id, line_id=line_id, add_qty=add_qty,
            set_qty=set_qty, display=display)

    @http.route(auth="user")
    def address(self, **kw):
        return super(WebsiteSale, self).address(**kw)

    @http.route(auth="user")
    def checkout(self, **post):
        return super(WebsiteSale, self).checkout(**post)

    @http.route(auth="user")
    def confirm_order(self, **post):
        return super(WebsiteSale, self).confirm_order(**post)

    @http.route(auth="user")
    def extra_info(self, **post):
        return super(WebsiteSale, self).extra_info(**post)

    @http.route(auth="user")
    def payment(self, **post):
        return super(WebsiteSale, self).payment(**post)

    @http.route(auth="user")
    def payment_transaction_token_confirm(self, tx, **kwargs):
        return super(WebsiteSale, self).payment_transaction_token_confirm(
            tx=tx, **kwargs)

    @http.route(auth="user")
    def payment_transaction_token(self, tx_id, **kwargs):
        return super(WebsiteSale, self).payment_transaction_token(
            tx_id=tx_id, **kwargs)

    @http.route(auth="user")
    def payment_transaction(self, acquirer_id, tx_type='form', token=None,
                            **kwargs):
        return super(WebsiteSale, self).payment_transaction(
            acquirer_id=acquirer_id, tx_type=tx_type, token=token)

    @http.route(auth="user")
    def payment_get_status(self, sale_order_id, **post):
        return super(WebsiteSale, self).payment_get_status(
            sale_order_id=sale_order_id, **post)

    @http.route(auth="user")
    def payment_validate(self, transaction_id=None, sale_order_id=None,
                         **post):
        return super(WebsiteSale, self).payment_validate(
            transaction_id=transaction_id, sale_order_id=sale_order_id, **post)

    @http.route(auth="user")
    def terms(self, **kw):
        return super(WebsiteSale, self).terms(**kw)

    @http.route(auth="user")
    def payment_confirmation(self, **post):
        return super(WebsiteSale, self).payment_confirmation(**post)

    @http.route(auth="user")
    def print_saleorder(self):
        return super(WebsiteSale, self).print_saleorder()

    @http.route(auth="user")
    def tracking_cart(self, **post):
        return super(WebsiteSale, self).tracking_cart(**post)

    @http.route(auth="user")
    def add_product(self, name=None, category=0, **post):
        return super(WebsiteSale, self).add_product(
            name=name, category=category, **post)

    @http.route(auth="user")
    def change_styles(self, id, style_id):
        return super(WebsiteSale, self).change_styles(id=id, style_id=style_id)

    @http.route(auth="user")
    def change_sequence(self, id, sequence):
        return super(WebsiteSale, self).change_sequence(
            id=id, sequence=sequence)

    @http.route(auth="user")
    def country_infos(self, country, mode, **kw):
        return super(WebsiteSale, self).country_infos(
            country=country, mode=mode, **kw)
