import re
import pandas as pd

def extract(file):
   with open(file, 'r', newline='', encoding='utf-8') as f:
    scores = []
    for line in f:    
        matches = re.findall(r'\d{1,3}.*?\d{2}\:\d{2}',line)
        if matches:
            scores.extend(matches)

    mtch = lambda score: re.match(r'(?P<position>\d{1,3})\s(?P<mw>[MW])(?P<score>\d{1,3}|ns)\s(?P<name>[\w\s\-]+?)\s*(?P<category>[MW]\d{1,3})?\sKent\s(?P<time>\d{2}\:\d{2})', score)

    kents = [(score, mtch(score)) for score in scores if mtch(score)]

    field = lambda kent, field: (field, kent[1].group(field))
    unpack = lambda kent: dict([field(kent,'position'), field(kent, 'mw'), field(kent,'score'), field(kent, 'name'), field(kent, 'category'), field(kent, 'time')])

    records = list(map(unpack, kents))
    assert len(records) == 39
    df = pd.DataFrame.from_dict(records)
    df = df.apply(pd.to_numeric, errors='ignore')
    print(df.dtypes)

    df_w = df.loc[df.mw == 'W'] 
    df_m = df.loc[df.mw == 'M']

    return df_w, df_m