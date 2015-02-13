# This file is part galatea_tutorial module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from .configuration import *
from .tutorial import *
from .galatea import *

def register():
    Pool.register(
        Configuration,
        GalateaTutorial,
        GalateaTutorialWebSite,
        GalateaTutorialComment,
        GalateaWebSite,
        module='galatea_tutorial', type_='model')
