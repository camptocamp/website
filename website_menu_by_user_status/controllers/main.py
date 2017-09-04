# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import http
from odoo.http import request

from odoo.addons.web.controllers.main import Home


class Website(Home):

    def _get_pages(self):
        """
        All pages width url
        """
        return request.env['website.menu'].sudo().search([]).filtered('url')

    def _check_user_access(self):
        """
        Is user logged
        """
        return request.env.user == request.website.user_id or False

    def _get_suggest_page(self):
        """
        All pages accessible by the user (logged or not)
        """
        if self._check_user_access():
            return self._get_pages().filtered(lambda r: r.user_not_logged)
        else:
            return self._get_pages().filtered(lambda r: r.user_logged)

    def _get_page_access(self, url):
        # active pages
        active_urls = self._get_pages()

        # compose access page url
        base_url = u'/page/'
        base_url += url

        # check Public user or Logged user
        if self._check_user_access():
            return active_urls.filtered(
                lambda r: r.user_not_logged and r.url == base_url)
        else:
            return active_urls.filtered(
                lambda r: r.user_logged and r.url == base_url)

    @http.route('/', type='http', auth="public", website=True)
    def index(self, **kw):
        # Do not return 404 for odoo backend menu
        main_menu = request.env.ref('website.main_menu',
                                    raise_if_not_found=False)
        if not main_menu:
            url = request.httprequest.referrer.split('/')[-1]
            to_display = self._get_page_access(url)
            if not len(to_display) > 0:
                return request.render('website.404', {
                    'suggest_page': self._get_suggest_page(),
                })
        return super(Website, self).index(**kw)

    @http.route('/page/<page:page>', type='http', auth="public", website=True,
                cache=300)
    def page(self, page, **opt):
        to_display = self._get_page_access(page)
        if len(to_display) > 0:
            return super(Website, self).page(page, **opt)
        return request.render('website.404', {
            'suggest_page': self._get_suggest_page(),
        })
