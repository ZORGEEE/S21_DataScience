import sys

def show_name():

    COMPANIES = {
        'Apple': 'AAPL',
        'Microsoft': 'MSFT',
        'Netflix': 'NFLX',
        'Tesla': 'TSLA',
        'Nokia': 'NOK'
        }

    STOCKS = {
        'AAPL': 287.73,
        'MSFT': 173.79,
        'NFLX': 416.90,
        'TSLA': 724.88,
        'NOK': 3.37
        }

    if len(sys.argv) != 2:
        print("Error. Expected ONE argument.")
        return
    
    ticker = sys.argv[1].upper()
    
    TICKER_TO_COMPANY = {v: k for k, v in COMPANIES.items()}
    
    if ticker in TICKER_TO_COMPANY and ticker in STOCKS:
        company_name = TICKER_TO_COMPANY[ticker]
        stock_price = STOCKS[ticker]
        print(f"{company_name} {stock_price}")
    else:
        print("Unknown ticker")

if __name__ == "__main__":
    show_name()
