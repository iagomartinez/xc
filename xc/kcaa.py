import re
import pandas as pd

def extract_row(line):
    resultex = r'\d{1,3}\s\d{1,3}\s.*?\d{1,2}\:\d{1,2}'
    return re.findall(resultex,line)

def extract_file(file):
    results = []
    with open(file, 'r', newline='', encoding='utf-8') as f:
        for line in f:
            results.extend(extract_row(line))
    return results