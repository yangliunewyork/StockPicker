#!/usr/bin/python

import sys
import argparse
import time

from Model.Stock import Stock
from DataCollector.NasdaqDataCollector import NasdaqDataCollector
from DataCollector.YahooFinanceDataCollector import YahooFinanceDataCollector
from DataCollector.StockAnalysisWebsiteDataCollector import StockAnalysisWebsiteDataCollector
from DataCollector.GuruFocusDataCollector import GuruFocusDataCollector
from InvestmentStrategy.PersonalStrategy import PersonalStrategy
from Utils.IntrinsicValueCalculator import IntrinsicValueCalculator

def call_data_collectors(stocks):
    """
    Call different data collectors to popuplate Stock instances' fields.
    """
    # Data collectors
    yahooFinanceDataCollector = YahooFinanceDataCollector()
    stockAnalysisWebsiteDataCollector = StockAnalysisWebsiteDataCollector()
    guruFocusDataCollector = GuruFocusDataCollector()

    sleep_time = 30

    for stock in stocks:
        yahooFinanceDataCollector.get_stock_info(stock)
        stockAnalysisWebsiteDataCollector.get_stock_info(stock)
        guruFocusDataCollector.get_stock_info(stock)
        time.sleep(sleep_time)
        print ("Sleep {} seoncds to avoid being blocked by website".format(sleep_time))

def calculate_intrinsic_value(stocks):
    perpetualGrowthRate = 0.02 # Choose inflation rate.
    intrinsicValueCalculator = IntrinsicValueCalculator()
    for stock in stocks:
        stock.m_intrinsic_value = intrinsicValueCalculator.calculateIntrinsicValueBasedOnDiscountedCashFlow(
            stock.m_free_cash_flow_per_share,
            stock.m_free_cash_flow_per_share_growth_rate,
            stock.m_weighted_average_cost_of_capital_ratio,
            perpetualGrowthRate
        )

def recommend_good_stocks(stocks):
    """
    Recommend good stocks based on stocks information.
    """
    personal_strategy = PersonalStrategy()
    good_stocks = []
    for stock in stocks:
        if personal_strategy.stock_validation(stock) :
            good_stocks.append(stock)

    # Sorting and printing
    good_stocks.sort(key=lambda x: (x.m_price, -x.m_price_to_book_ratio), reverse=False)
    print("Good stocks : ", str(len(good_stocks)))
    for stock in good_stocks:
        print(stock.to_json())
    sys.exit(0)


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

    # Initialize a list of Stock instances with only m_symbol field value populated
    stocks = []
    for ticker in tickers:
        stock = Stock()
        stock.m_symbol = ticker
        stocks.append(stock)

    call_data_collectors(stocks)
    calculate_intrinsic_value(stocks)

    for stock in stocks:
        print(stock.to_json())

    recommend_good_stocks(stocks)

if __name__ == "__main__":
    main(sys.argv)

