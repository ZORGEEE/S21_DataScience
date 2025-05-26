import sys

def display_stocks():

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
        return
    
    input_string = sys.argv[1].strip()
    
    # Check for empty input or any form of consecutive commas (with or without spaces)
    if not input_string or any(x.strip() == '' for x in input_string.split(',')):
        return

    # Create case-insensitive mappings
    ticker_to_company = {v.lower(): k for k, v in COMPANIES.items()}
    company_lower = {k.lower(): k for k in COMPANIES}
    
    expressions = [x.strip() for x in input_string.split(',')]
    
    for expr in expressions:
        expr_lower = expr.lower()
        if expr_lower in ticker_to_company:
            company = ticker_to_company[expr_lower]
            print(f"{expr.upper()} is a ticker symbol for {company}")
        elif expr_lower in company_lower:
            company = company_lower[expr_lower]
            ticker = COMPANIES[company]
            price = STOCKS[ticker]
            print(f"{company} stock price is {price}")
        else:
            print(f"{expr} is an unknown company or an unknown ticker symbol")


if __name__ == "__main__":
    display_stocks()