#!/usr/bin/env python3
import sys
import pytest
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
        head = parts[0].capitalize() + " " + parts[1].capitalize()
        if head.lower() == field.lower():
            values = parts[2:]
            output = (head,) + tuple(values)
            return output
    raise Exception(f"Field '{field}' not found for ticker '{ticker}'")
    

def test_valid_ticker_and_field():
    """Test that valid ticker and field returns correct data"""
    result = fetch_financials('AAPL', 'Total Revenue')
    assert isinstance(result, tuple)
    assert len(result) > 2  # At least field name and one value
    assert 'Total Revenue' in result[0]

def test_invalid_ticker():
    """Test that invalid ticker raises exception"""
    with pytest.raises(Exception):
        fetch_financials('INVALIDTICKER123', 'Total Revenue')

def test_invalid_field():
    """Test that invalid field raises exception"""
    with pytest.raises(Exception):
        fetch_financials('AAPL', 'Invalid Field Name')

def test_return_type():
    """Test that return type is always tuple"""
    result = fetch_financials('MSFT', 'Total Revenue')
    assert isinstance(result, tuple)

def test_field_matching():
    """Test that field name matching is case insensitive"""
    result1 = fetch_financials('GOOG', 'total revenue')
    result2 = fetch_financials('GOOG', 'Total Revenue')
    assert result1[0].lower() == result2[0].lower()

def test_data_consistency():
    """Test that same request returns consistent results"""
    result1 = fetch_financials('AMZN', 'Total Revenue')
    result2 = fetch_financials('AMZN', 'Total Revenue')
    assert result1[0] == result2[0]  # Field name should match
    assert len(result1) == len(result2)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        pytest.main([__file__])
    else:
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


# pytest -v для запуска понятного тестирования