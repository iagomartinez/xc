import pandas as pd
import sys
from pathlib import Path
import requests as req
from bs4 import BeautifulSoup
from time import sleep
import csv

ROOT = Path(__file__).parent.parent

def scrape(name):

    [fn,ln] = name.split()
    print([fn,ln])
    html_text = req.get(f'https://www.thepowerof10.info/athletes/athleteslookup.aspx?surname={ln}&firstname={fn}&club=Kent+AC').text
    soup = BeautifulSoup(html_text, 'html.parser')
    table = soup.find('table', attrs={'id':'cphBody_dgAthletes'})
    if table is None:
        print(f'Athlete {fn} {ln} not found')
        return [ln,fn,None,None]

    print(f'Athlete {fn} {ln} found')
    rows = list(table.find_all('tr'))
    cols = rows[1].find_all('td')
    category = cols[4].text.strip()
    runbritain_url = cols[8].a['href']

    print(runbritain_url)
    run_britain_text = req.get(runbritain_url).text
    soup = BeautifulSoup(run_britain_text, 'html.parser')
    handicap = soup.find('div', {'id': 'h-number'})
    
    print(fn, ln, handicap.text.strip())
    sleep(1)
    return [ln,fn,category,handicap.text.strip()]

def get_handicaps(inputfile, outputfile):
    with open(inputfile, 'r', newline='', encoding='utf-8') as f:
        with open(outputfile, 'w', newline='', encoding='utf-8') as outfile:
            writer=csv.writer(outfile)
            writer.writerow(['last_name', 'name', 'handicap'])
            for line in f:
                data = scrape(line.strip())
                writer.writerow(data)    

def main():
    get_handicaps(ROOT / 'data/men_names.txt', ROOT / 'data/men_handicaps.csv')
    get_handicaps(ROOT / 'data/women_names.txt', ROOT / 'data/women_handicaps.csv')

if __name__ == '__main__':
    sys.exit(main())