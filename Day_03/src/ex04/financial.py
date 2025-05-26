#!/usr/bin/env python3
import sys
import time
import requests
from bs4 import BeautifulSoup

def fetch_financials(ticker, field):
    # time.sleep(5)

    url = f'https://finance.yahoo.com/quote/{ticker}/financials'
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"URL not found or could not fetch data for {ticker}")

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('div', {"class": "tableBody"})

    for row in rows:
        label_div = row.find('div', {"class": "row"})
        if not label_div:
            continue
        label = label_div.text.strip()
        parts = label.split()
        head = parts[0] + " " + parts[1]
        values = parts[2:]
        output = (head,) + tuple(values)
        return output
    raise Exception(f"Field '{field}' not found for ticker '{ticker}'")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: ./financial.py 'TICKER' 'FIELD NAME'")
        sys.exit(1)

    ticker = sys.argv[1]
    field = sys.argv[2]

    try:
        result = fetch_financials(ticker, field)
        print(result)
    except Exception as e:
        print("Error:", e)
        sys.exit(1)
