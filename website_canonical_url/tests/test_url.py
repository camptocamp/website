# -*- coding: utf-8 -*-
# Copyright 2018 Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase
import mock


class FakeRequest(object):

    def __init__(self, website, path, lang='en_US'):
        self.website = website
        self.lang = lang
        self.httprequest = mock.MagicMock()
        self.httprequest.path = path


class URLCase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(URLCase, cls).setUpClass()
        cls.website = cls.env['website'].browse(1)
        cls.base_url = cls.env['ir.config_parameter'].get_param('web.base.url')

    def test_canonical_domain_default(self):
        self.assertEqual(
            self.website._get_canonical_domain(),
            self.base_url
        )

    def test_canonical_domain_custom(self):
        self.website.canonical_domain = 'https://oh.yeah'
        self.assertEqual(
            self.website._get_canonical_domain(),
            'https://oh.yeah'
        )

    def test_canonical_domain_protocol_validation(self):
        with self.assertRaises(exceptions.ValidationError):
            self.website.canonical_domain = 'oh.yeah'
        with self.assertRaises(exceptions.ValidationError):
            self.website.canonical_domain = 'http.yeah'

    def test_canonical_relative_url_nolang(self):
        req = FakeRequest(self.website, '/my/lovely/page?foo=baz')
        self.assertEqual(
            self.website._get_canonical_relative_url(req=req),
            '/my/lovely/page'
        )

    def test_canonical_relative_url_default_lang_match(self):
        req = FakeRequest(
            self.website, '/it_IT/my/lovely/page?foo=baz', lang='it_IT')
        self.website.default_lang_id = self.env.ref('base.lang_it')
        # actually, in this case, where the lang is the same of website
        # odoo will redirect to the root URL.
        # Here we just make sure that extra stuff is splitted out
        self.assertEqual(
            self.website._get_canonical_relative_url(req=req),
            '/it_IT/my/lovely/page'
        )

    def test_canonical_relative_url_default_lang_no_match(self):
        req = FakeRequest(self.website, '/en_US/my/lovely/page?foo=baz')
        self.website.default_lang_id = self.env.ref('base.lang_it')
        self.assertEqual(
            self.website._get_canonical_relative_url(req=req),
            '/en_US/my/lovely/page'
        )

    def test_canonical_relative_url_home_special_case(self):
        req = FakeRequest(self.website, '/page/homepage?foo=baz', lang='it_IT')
        self.website.default_lang_id = self.env.ref('base.lang_it')
        self.assertEqual(
            self.website._get_canonical_relative_url(req=req),
            '/'
        )

    def test_canonical_relative_url_home_special_case_lang_no_match(self):
        req = FakeRequest(self.website, '/en_US/page/homepage?foo=baz')
        self.website.default_lang_id = self.env.ref('base.lang_it')
        self.assertEqual(
            self.website._get_canonical_relative_url(req=req),
            '/en_US'
        )

    def test_canonical_url(self):
        self.website.canonical_domain = 'https://oh.yeah'
        req = FakeRequest(self.website, '/page/foo?foo=baz')
        self.assertEqual(
            self.website.get_canonical_url(req=req),
            'https://oh.yeah/page/foo'
        )

    def test_canonical_url_default_lang_no_match(self):
        self.website.canonical_domain = 'https://oh.yeah'
        req = FakeRequest(self.website, '/en_US/my/lovely/page?foo=baz')
        self.website.default_lang_id = self.env.ref('base.lang_it')
        self.assertEqual(
            self.website.with_context(lang='en_US').get_canonical_url(req=req),
            'https://oh.yeah/en_US/my/lovely/page'
        )

    def test_canonical_url_home_special_case(self):
        self.website.canonical_domain = 'https://oh.yeah'
        req = FakeRequest(self.website, '/page/homepage?foo=baz')
        self.assertEqual(
            self.website.get_canonical_url(req=req),
            'https://oh.yeah/'
        )

    def test_canonical_url_home_special_case_no_match(self):
        self.website.canonical_domain = 'https://oh.yeah'
        req = FakeRequest(
            self.website, '/it_IT/page/homepage?foo=baz', lang='it_IT')
        self.assertEqual(
            self.website.get_canonical_url(req=req),
            'https://oh.yeah/it_IT'
        )
