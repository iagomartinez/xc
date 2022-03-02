import re
import pandas as pd
import sys
from pathlib import Path
from IPython.display import display

ROOT = Path(__file__).parent.parent

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
    RESULT_REGEX = r'(?P<position>\d{1,3})\s(?:\d{1,3})\s(?P<name>.*?)\s(?:\((?P<category>\w*)\)\s)?(?P<club>[\w&]*)\s(?P<time>\d{1,2}\:\d{1,2})'

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

def as_dataframe(parsed):
    df = pd.DataFrame.from_records(parsed)
    df = df.loc[df.club == 'KENT']
    df = df.apply(pd.to_numeric, errors='ignore')
    df.sort_values(by='position', inplace=True)
    return df

def main():
    rp = ResultParser()

    data = ROOT / 'data'

    results = extract_file(data / 'kent_champs_men.txt')
    df_men = as_dataframe(parse(results))
    assert len(df_men.index) == 21
    df_men.to_csv(data / 'parsed_kcaa_men.csv', index=False)

    results = extract_file(data / 'kent_champs_women.txt')
    df_men = as_dataframe(parse(results))
    assert len(df_men.index) == 13
    df_men.to_csv(data / 'parsed_kcaa_women.csv', index=False)

    print('Export completed!')

if __name__ == '__main__':
    sys.exit(main())    