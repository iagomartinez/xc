import pandas as pd
import sys
from pathlib import Path
import requests as req
from bs4 import BeautifulSoup
from IPython.display import display

ROOT = Path(__file__).parent.parent

def scrape(pages, table_header, table_id, row_fn, expected_count):
    data = []

    for page_url in pages:
        print(f'get {page_url}')
        html_text = req.get(page_url).text
        soup = BeautifulSoup(html_text, 'html.parser')

        table = soup.find('table', attrs={'id':table_id})
        assert table is not None
        elem = soup.find(text=table_header)
        assert elem is not None
        elem = elem.find_parent('tr')
        header = elem.find_next_sibling('tr')
        assert elem is not None
        rows = header.find_next_siblings('tr')
        for r in rows:
            row = r.find_all("td")
            if len(row) == 1:
                break
            data.append(row_fn(row))

    df = pd.DataFrame.from_dict(data)
    df = df.loc[(df.club == 'Kent') | (df.club == 'Kent AC') | (df.club.str.startswith('Kent'))]
    assert len(df.index) == expected_count, f'{len(df.index)}'

    df['position'] = df['position'].astype(int)
    df.sort_values(by='position', inplace=True)

    df['rank'] = df['position'].rank(method='first').astype(int)
    df = df[['rank','position', 'time', 'category', 'name']]
    return df

def main():

    # SOTCCA 5M 2023
    # row_fn = lambda row: {'position':row[0].text, 'time':row[3].text, 'name':row[4].text, 'category':row[5].text,'mw':row[6].text, 'club':row[8].text}
    # df_sotcca = scrape(['https://www.thepowerof10.info/results/results.aspx?meetingid=502627'], '5MXC', 'cphBody_dgP', row_fn,38)
    # df_m = df_sotcca.loc[df_sotcca.mw == "M"].copy()
    # df_m['rank'] = df_m['position'].rank(method='first').astype(int)
    # df_m.to_csv(ROOT / 'data/sotcca_5M_kent_men.csv', index=False)

    # df_w = df_sotcca.loc[df_sotcca.mw == "W"].copy()
    # df_w['rank'] = df_w['position'].rank(method='first').astype(int)
    # df_w.to_csv(ROOT / 'data/sotcca_5M_kent_women.csv', index=False)

    # SOTCCA 7.5M 2023
    # row_fn = lambda row: {'position':row[0].text, 'time':row[3].text, 'name':row[4].text, 'category':row[5].text,'mw':row[6].text, 'club':row[8].text}
    # df_sotcca = scrape(['https://www.thepowerof10.info/results/results.aspx?meetingid=506441'], '7.5MXC', 'cphBody_dgP', row_fn,7)
    # df_m = df_sotcca.loc[df_sotcca.mw == "M"].copy()
    # df_m['rank'] = df_m['position'].rank(method='first').astype(int)
    # df_m.to_csv(ROOT / 'data/sotcca_champs_kent_men.csv', index=False)

    # Kent Champs 2023
    # row_fn = lambda row: {'position':row[0].text, 'time':row[2].text, 'name':row[3].text, 'category':row[4].text,'mw':row[5].text, 'club':row[8].text}
    # df_kc_m = scrape(['https://www.thepowerof10.info/results/results.aspx?meetingid=510884&pagenum=2#12KXC','https://www.thepowerof10.info/results/results.aspx?meetingid=510884&pagenum=3'], '12KXC SM', 'cphBody_dgP', row_fn,16)
    # df_kc_m.to_csv(ROOT / 'data/kent_champs_men.csv', index=False)

    #Women
    # row_fn = lambda row: {'position':row[0].text, 'time':row[2].text, 'name':row[3].text, 'category':row[4].text,'mw':row[5].text, 'club':row[8].text}
    # df_kc_m = scrape(['https://www.thepowerof10.info/results/results.aspx?meetingid=510884&pagenum=1#8.35KXC','https://www.thepowerof10.info/results/results.aspx?meetingid=510884&pagenum=2'], '8.35KXC SW', 'cphBody_dgP', row_fn,13)
    # df_kc_m.to_csv(ROOT / 'data/kent_champs_women.csv', index=False)

    # SL 3 2023
    #row_fn = lambda row: {'position':row[0].text, 'time':row[2].text, 'name':row[3].text, 'category':row[4].text,'mw':row[5].text, 'club':row[8].text}

    # df_m = scrape(['https://www.thepowerof10.info/results/results.aspx?meetingid=443285', 'https://www.thepowerof10.info/results/results.aspx?meetingid=443285&pagenum=2'], '8KXC SM', 'cphBody_dgP', row_fn,221)
    # df_m.to_csv(ROOT / 'data/sl3_kent_men.csv', index=False)

    # df_w = scrape(['https://www.thepowerof10.info/results/results.aspx?meetingid=444365&pagenum=1','https://www.thepowerof10.info/results/results.aspx?meetingid=444365&pagenum=2'],'8KXC SW D1', 'cphBody_dgP', row_fn,221)
    # df_w.to_csv(ROOT / 'data/sl3_kent_women.csv', index=False)

if __name__ == '__main__':
    sys.exit(main())