# -*- coding: utf-8 -*-
# Copyright 2018 Simone Orsi <simone.orsi@camptocamp.com>
# Copyright initOS GmbH 2016
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields
from odoo.http import request
from urlparse import urlparse, urlunparse, urljoin


class Website(models.Model):
    _inherit = 'website'

    canonical_domain = fields.Char()

    @api.multi
    def get_canonical_url(self, req=None):
        return urljoin(
            self._get_canonical_domain(),
            self._get_canonical_relative_url(req=req)
        )

    @api.multi
    def _get_canonical_domain(self):
        self.ensure_one()
        if self.canonical_domain:
            return self.canonical_domain
        params = self.env['ir.config_parameter'].sudo()
        return params.get_param('web.base.url')

    @api.multi
    def _get_canonical_relative_url(self, req=None):
        req = req or request
        parsed = urlparse(req.httprequest.path)
        canonical_url = parsed.path
        lang = (
            getattr(req, 'lang', None) or
            self.env.lang or
            req.website.default_lang_code
        )
        lang_path = ''
        if lang != req.website.default_lang_code:
            # eg: language is `it_IT` but main lang is `en_US`
            lang_path = '/%s/' % lang
        if lang_path and not canonical_url.startswith(lang_path):
            # not main lang: make sure lang is in path
            canonical_url = lang_path + canonical_url.lstrip('/')
        # Special case for rerouted requests to root path
        if self._is_root_page(canonical_url, lang_path=lang_path):
            # redirect to root if main lang otherwise to language root
            canonical_url = '/' if not lang_path else lang_path.rstrip('/')
        return canonical_url

    def _is_root_page(self, url, lang_path=''):
        # TODO v11: `/page` does not exist anymore
        first_part = '/page/'
        if lang_path:
            # usually URLs in menu item do not contain lang
            url = url.replace(lang_path, '/')
        return (
            url.startswith(first_part) and
            self.menu_id.child_id and
            self.menu_id.child_id[0].url == url
        )
