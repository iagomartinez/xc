import re
import pandas as pd

def parse_entries(line):
    resultex = r'\d{1,3}\s\d{1,3}\s.*?\d{1,2}\:\d{1,2}'
    return re.findall(resultex,line)