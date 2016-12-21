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
def admin_user_password(ctx):
    # password for the test server,
    # the password must be changed in production
    ctx.env.user.password_crypt = (
        '$pbkdf2-sha512$19000$wThnDOH83/v/////XwvBmA$H5YDmNbV/XbFj1Z5tuUhp'
        '.Yb9.sYXrGKAUOETx/wJW7DMl4jMU7OPUQVWTk/ufzjDCenvJg4FgnSJxLML0vGlw'
    )


@anthem.log
def main(ctx):
    """ Main: creating demo data """
    load_users(ctx)
    admin_user_password(ctx)
