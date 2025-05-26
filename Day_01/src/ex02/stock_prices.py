import sys

def show_price():

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
    
    company = sys.argv[1]
    c_name = company.title()

    if c_name in COMPANIES:
        ticker = COMPANIES[c_name]
        print(STOCKS[ticker])
    else:
        print("Unknown company")

if __name__ == "__main__":
    show_price()
