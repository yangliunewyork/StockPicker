#!/usr/bin/python

import sys
import argparse
from Model.Stock import Stock
from DataCollector.NasdaqDataCollector import NasdaqDataCollector
from DataCollector.YahooFinanceDataCollector import YahooFinanceDataCollector
from DataCollector.StockAnalysisWebsiteDataCollector import StockAnalysisWebsiteDataCollector
from InvestmentStrategy.PersonalStrategy import PersonalStrategy

def main(argv):
    argumentParser = argparse.ArgumentParser(description='Command list.')
    argumentParser.add_argument('-t','--tickers', nargs='+', help='StockPicker.py -t AAPL AMZN', required=False)
    args = argumentParser.parse_args()

    tickers = []
    if args.tickers:
        tickers = args.tickers
    else:    
        nasdaqDataCollector = NasdaqDataCollector()
        tickers = nasdaqDataCollector.get_tickers()
        print("Total stocks in Nasdaq: " , str(len(tickers)))
        tickers = tickers

    stocks = []
    for ticker in tickers:
        stock = Stock()
        stock.m_symbol = ticker
        stocks.append(stock)

    yahooFinanceDataCollector = YahooFinanceDataCollector()
    #tickers = ["GOOG","FB","GILD","AAPL"]
    for stock in stocks:
        yahooFinanceDataCollector.get_stock_info(stock)


    stockAnalysisWebsiteDataCollector = StockAnalysisWebsiteDataCollector()
    for stock in stocks:
        stockAnalysisWebsiteDataCollector.get_stock_info(stock)

    personal_strategy = PersonalStrategy()
    good_stocks = []
    for stock in stocks:
        print(stock.to_json())
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

