# -*- coding: utf-8 -*-
# Copyright 2019 Camptocamp (http://www.camptocamp.com)
# Simone Orsi <simone.orsi@camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models
from openerp import fields
from openerp import api
from openerp import tools



class Website(models.Model):
    """Override website model."""

    _inherit = "website"

    def get_alternate_languages(self, cr, uid, ids,
                                req=None, context=None,
                                main_object=None):
        langs = super(Website, self).get_alternate_languages(
            cr, uid, ids, req=req, context=context)

        avail_langs = None
        if main_object and hasattr(main_object, 'get_translations'):
            # avoid building URLs for not translated contents
            avail_transl = main_object.get_translations()
            avail_langs = [x.split('_')[0] for x in avail_transl.iterkeys()]

        if avail_langs is not None:
            langs = [lg for lg in langs if lg['short'] in avail_langs]
        return langs

    def translation_needs_review(self, main_object):
        if main_object and 'translation_review_required' in main_object:
            return main_object.translation_review_required
        return False


class WebsiteMixin(models.Model):
    """Override website model."""
    _inherit = "website.published.mixin"

    translation_review_required = fields.Boolean(
        string='Translation review required',
        default=True,
    )

    @api.model
    def get_translations(self):
        """Return translations for this page."""
        return self._get_translations(rec_id=self.id, rec_model=self._name)

    @tools.ormcache('page_id', 'rec_model')
    def _get_translations(self, rec_id=None, rec_model=None):
        """Return all available translations for a page.

        IMPORTANT: we assume that a page is translated when the name is
        as it's next to impossible to determine if a page is fully translated.
        """
        # TODO: tackle sql-injection warning
        query = """
            SELECT lang,value FROM ir_translation
            WHERE res_id={rec_id}
            AND state='translated'
            AND type='model'
            AND name='{rec_model},name'
        """.format(rec_id=rec_id, rec_model=rec_model)
        self.env.cr.execute(query)
        res = self.env.cr.fetchall()
        return dict(res)
