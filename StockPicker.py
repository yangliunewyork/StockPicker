#!/usr/bin/python

import sys
import argparse
from Model.Stock import Stock
from DataCollector.NasdaqTracker import NasdaqTracker
from DataCollector.YahooFinanceTracker import YahooFinanceTracker
from InvestmentStrategy.PersonalStrategy import PersonalStrategy

def main(argv):
    argumentParser = argparse.ArgumentParser(description='Command list.')
    argumentParser.add_argument('-t','--tickers', nargs='+', help='StockPicker.py -t AAPL AMZN', required=False)
    args = argumentParser.parse_args()

    tickers = []
    if args.tickers:
        tickers = args.tickers
    else:    
        nasdaq_tracker = NasdaqTracker()
        nasdaq_tickers = nasdaq_tracker.get_tickers()
        print("Total stocks in Nasdaq: " , str(len(nasdaq_tickers)))
        tickers = nasdaq_tickers


    yahoo_tracker = YahooFinanceTracker()
    #tickers = ["GOOG","FB","GILD","AAPL"]
    yahoo_stocks = yahoo_tracker.get_data_from_yahoo(tickers)
    personal_strategy = PersonalStrategy()
    good_stocks = []
    for stock in yahoo_stocks:
        if personal_strategy.stock_validation(stock) :
            good_stocks.append(stock)

    # Sorting and printing
    good_stocks.sort(key=lambda x: x.m_price_to_book_ratio, reverse=False)
    print("Good stocks : ", str(len(good_stocks)))
    for stock in good_stocks:
        print(stock.to_json())
    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv)

