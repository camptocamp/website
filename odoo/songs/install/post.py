# -*- coding: utf-8 -*-
# Copyright 2016 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import anthem
from anthem.lyrics.loaders import load_csv
from pkg_resources import resource_filename

from ..common import req


@anthem.log
def load_users(ctx):
    csv_content = resource_filename(req, 'data/install/res.users.csv')
    load_csv(ctx, 'res.users', csv_content)


@anthem.log
def main(ctx):
    """ Main: creating demo data """
    load_users(ctx)
