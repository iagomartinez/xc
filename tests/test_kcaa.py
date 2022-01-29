import sys
import unittest
from pathlib import Path
import re
import pandas as pd
ROOT = Path(__file__).parent.parent

sys.path.insert(1, '..')
from xc import kcaa

class TestKentXc(unittest.TestCase):
    def test_extract_result(self):
        testdata = [('1 887 Jamie Goodge TON 41:41 61 741 Huntley Roberts (M35) DART 49:58', 2), ('144 645 Steve Hodges (M55) A&D 57:45',1)]
        for line, expectedcount in testdata:
            with self.subTest(f'testing {line}->{expectedcount}'):
                matches = kcaa.extract_result(line)
                self.assertEqual(expectedcount, len(matches))
    
    def test_extract_file(self):
        file = ROOT / 'data/kent_champs_men.txt'
        results = kcaa.extract_file(file)
        self.assertEqual(203, len(results))

    def test_parse_men(self):
        file = ROOT / 'data/kent_champs_men.txt'
        results = kcaa.extract_file(file)
        parsed = kcaa.parse(results)
        self.assertEqual(203, len(parsed))

    def test_parse_women(self):
        file = ROOT / 'data/kent_champs_women.txt'
        results = kcaa.extract_file(file)
        parsed = kcaa.parse(results)
        self.assertEqual(114, len(parsed))

    def test_ResultParser(self):
        rp = kcaa.ResultParser()
        testdata = [('16 812 Christopher McGurk KENT 45:10', {'position':'16', 'name': 'Christopher McGurk', 'club': 'KENT','category':None, 'time': '45:10'}),
            ('82 729 Johnnie Arnould (M40) CPA 51:58', {'position':'82', 'name': 'Johnnie Arnould', 'club': 'CPA', 'category':'M40','time': '51:58'}),
            ('10 489 Carole Coulon (W45) B&B 36:37', {'position':'10', 'name':'Carole Coulon', 'category':'W45', 'club':'B&B', 'time':'36:37'})]
        for input, expected in testdata:
            with self.subTest(f'testing {input}->{expected}'):
                parsed = rp.parse(input)
                self.assertDictEqual(expected, parsed)
        