# This file is part of the galatea_tutorial module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class GalateaTutorialTestCase(ModuleTestCase):
    'Test Galatea Tutorial module'
    module = 'galatea_tutorial'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        GalateaTutorialTestCase))
    return suite