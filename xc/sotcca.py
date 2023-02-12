import re
import pandas as pd

def extract(file, expected_records):
    with open(file, 'r', newline='', encoding='utf-8') as f:
        scores = []
        for line in f:    
            matches = re.findall(r'\d{1,3}.*?\d{2}\:\d{2}',line)
            if matches:
                scores.extend(matches)
    #print(scores)

    print(f'scores found: {len(scores)}')
#($|\s)(?P<position>[W]*\d{1,3}(x*))\s(?P<name>[\w\s\-]+?)\s*(?P<category>[MW]\d{1,3})?\sKent\s(?P<time>\d{2}\:\d{2})
    mtch = lambda score: re.match(r'(?P<mw>[W])?(?P<position>\d{1,3})x*\s(?P<name>[\w\s\-]+?)\s*(?P<category>[MW]\d{1,3})?\sKent\s(?P<time>\d{2}\:\d{2})', score)

    kents = [(score, mtch(score)) for score in scores if mtch(score)]
    assert kents is not None, 'kents is None'
    print(f'kents found: {len(kents)}')

    #field = lambda kent, field: (field, kent[1].group(field))
    unpack = lambda match: match.groupdict()

    records = list(map(unpack, kents))
    assert records is not None, 'records is None'

    assert len(records) == expected_records, f'found {len(records)}, expected {expected_records}'
    df = pd.DataFrame.from_dict(records)
    df = df.apply(pd.to_numeric, errors='ignore')
    print(df.dtypes)

    df_w = df.loc[df.mw == 'W'] 
    df_m = df.loc[df.mw == 'M']

    return df_w, df_m