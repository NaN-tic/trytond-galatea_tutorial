# This file is part galatea_tutorial module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Configuration']
__metaclass__ = PoolMeta


class Configuration:
    __name__ = 'galatea.configuration'
    tutorial_thumb_size = fields.Integer('Tutorial Thumb Size',
        help='Thumbnail Tutorial Image Size (width x height)')
    tutorial_thumb_crop = fields.Boolean('Tutorial Thumb Crop',
        help='Crop Thumb Tutorial Image')

    @staticmethod
    def default_tutorial_thumb_size():
        return 300
