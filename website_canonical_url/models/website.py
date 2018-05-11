# -*- coding: utf-8 -*-
# Copyright 2018 Simone Orsi <simone.orsi@camptocamp.com>
# Copyright initOS GmbH 2016
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, api, fields, exceptions, _
from odoo.http import request
from urlparse import urlparse, urljoin


class Website(models.Model):
    _inherit = 'website'

    canonical_domain = fields.Char(
        help='Canonical domain is used to build unique canonical URLs '
             'to make SEO happy.'
    )

    @api.constrains('canonical_domain')
    def _check_canonical_domain(self):
        domain = self.canonical_domain
        if domain and not urlparse(domain).scheme:
            raise exceptions.ValidationError(_(
                'Canonical domain must contain protocol `http(s)://`'
            ))

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
        # here we get the full path and qstring args stripped out already
        canonical_url = parsed.path
        # build lang path if request lang does not match default lang
        lang_path = ''
        if req.lang != req.website.default_lang_code:
            # eg: language is `it_IT` but main lang is `en_US`
            lang_path = '/%s/' % req.lang
        # handle special case for rerouted requests to root path
        if self._is_root_page(canonical_url, lang_path=lang_path):
            # redirect to root if main lang matches otherwise to language root
            canonical_url = '/' if not lang_path else lang_path
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
