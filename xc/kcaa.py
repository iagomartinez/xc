from mimetypes import init
import re
from types import new_class
import pandas as pd

def extract_result(line):
    resultex = r'\d{1,3}\s\d{1,3}\s.*?\d{1,2}\:\d{1,2}'
    return re.findall(resultex,line)

def extract_file(file):
    results = []
    with open(file, 'r', newline='', encoding='utf-8') as f:
        for line in f:
            results.extend(extract_result(line))
    return results

class ResultParser():
    RESULT_REGEX = r'(?P<position>\d{1,3})\s(?:\d{1,3})\s(?P<name>.*?)\s(?P<club>[\w&]*)\s(?P<time>\d{1,2}\:\d{1,2})'

    def __init__(self):
        self.resultx = re.compile(self.RESULT_REGEX)

    def parse(self, result):
        m = self.resultx.match(result)
        if not m:
            raise Exception(f'failed to parse row {result}')
        return m.groupdict()

def parse(results):
    rp = ResultParser()
    return [rp.parse(result) for result in results]