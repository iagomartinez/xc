import sys
import unittest
from pathlib import Path
import re
import pandas as pd
THIS_DIR = Path(__file__).parent

sys.path.insert(1, '..')
from xc import kcaa

class TestKentXc(unittest.TestCase):
    def test_parse_entries(self):
        testdata = [('1 887 Jamie Goodge TON 41:41 61 741 Huntley Roberts (M35) DART 49:58', 2), ('144 645 Steve Hodges (M55) A&D 57:45',1)]
        for line, expectedcount in testdata:
            with self.subTest(f'testing {line}->{expectedcount}'):
                matches = kcaa.parse_entries(line)
                self.assertEquals(expectedcount, len(matches))
