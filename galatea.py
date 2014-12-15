# This file is part galatea_tutorial module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval

__all__ = ['GalateaWebSite']
__metaclass__ = PoolMeta


class GalateaWebSite:
    __name__ = "galatea.website"
    tutorial_comment = fields.Boolean('Tutorial Comments',
        help='Active tutorial comments.')
    tutorial_anonymous = fields.Boolean('Tutorial Anonymous',
        help='Active user anonymous to publish comments.')
    tutorial_anonymous_user = fields.Many2One('galatea.user', 'Tutorial Anonymous User',
        states={
            'required': Eval('tutorial_anonymous', True),
        })
