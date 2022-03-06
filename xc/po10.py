import pandas as pd
import sys
from pathlib import Path
import requests as req
from bs4 import BeautifulSoup

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

    assert len(data) == expected_count, f'{len(data)}'
    df = pd.DataFrame.from_dict(data)
    df = df.loc[df.club == 'Kent']
    return df

def main():

    #with open(file, 'r', newline='', encoding='utf-8') as f:
    #    html_text = f.read()

    # pages =
    #     table = soup.find('table', attrs={'id':'cphBody_dgP'})
    #     elem = soup.find(text='8KXC SM')

    # df_m = scrape(['https://www.thepowerof10.info/results/results.aspx?meetingid=443285', 'https://www.thepowerof10.info/results/results.aspx?meetingid=443285&pagenum=2'], '8KXC SM', 'cphBody_dgP')
    # df_m.to_csv(ROOT / 'data/sl3_kent_men.csv', index=False)

    # df_w = scrape(['https://www.thepowerof10.info/results/results.aspx?meetingid=444365&pagenum=1','https://www.thepowerof10.info/results/results.aspx?meetingid=444365&pagenum=2'],'8KXC SW D1', 'cphBody_dgP')
    # df_w.to_csv(ROOT / 'data/sl3_kent_women.csv', index=False)


    # pages = ['https://www.thepowerof10.info/results/results.aspx?meetingid=450428&top=6000&pagenum=10#8KXC',
    #     'https://www.thepowerof10.info/results/results.aspx?meetingid=450428&top=6000&pagenum=11',
    #     'https://www.thepowerof10.info/results/results.aspx?meetingid=450428&top=6000&pagenum=12',
    #     'https://www.thepowerof10.info/results/results.aspx?meetingid=450428&top=6000&pagenum=13',
    #     'https://www.thepowerof10.info/results/results.aspx?meetingid=450428&top=6000&pagenum=14']

    # row_fn = lambda row: {'position':row[0].text, 'time':row[1].text, 'name':row[2].text, 'category':row[3].text, 'club':row[7].text}

    # df_w = scrape(pages,'8KXC SW', 'cphBody_dgP', row_fn, 1011)
    # df_w.to_csv(ROOT / 'data/national_kent_women.csv', index=False)


    pages = ['https://www.thepowerof10.info/results/results.aspx?meetingid=450428&top=6000&pagenum=15#12KXC',
        'https://www.thepowerof10.info/results/results.aspx?meetingid=450428&top=6000&pagenum=16',
        'https://www.thepowerof10.info/results/results.aspx?meetingid=450428&top=6000&pagenum=17',
        'https://www.thepowerof10.info/results/results.aspx?meetingid=450428&top=6000&pagenum=18',
        'https://www.thepowerof10.info/results/results.aspx?meetingid=450428&top=6000&pagenum=19',
        'https://www.thepowerof10.info/results/results.aspx?meetingid=450428&top=6000&pagenum=20',
        'https://www.thepowerof10.info/results/results.aspx?meetingid=450428&top=6000&pagenum=21',
        'https://www.thepowerof10.info/results/results.aspx?meetingid=450428&top=6000&pagenum=22',
        'https://www.thepowerof10.info/results/results.aspx?meetingid=450428&top=6000&pagenum=23']

    row_fn = lambda row: {'position':row[0].text, 'time':row[1].text, 'name':row[2].text, 'category':row[3].text, 'club':row[7].text}

    df = scrape(pages,'12KXC SM', 'cphBody_dgP', row_fn, 2089)
    df.to_csv(ROOT / 'data/national_kent_men.csv', index=False)



if __name__ == '__main__':
    sys.exit(main())