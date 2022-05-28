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
    guruFocusDataCollector = GuruFocusDataCollector()

    # Disable it as it has a rate limit that requires 30 seconds apart
    #stockAnalysisWebsiteDataCollector = StockAnalysisWebsiteDataCollector() 

    sleep_time = 2

    for stock in stocks:
        yahooFinanceDataCollector.get_stock_info(stock)
        #stockAnalysisWebsiteDataCollector.get_stock_info(stock)
        guruFocusDataCollector.get_stock_info(stock)
        time.sleep(sleep_time)
        print ("Sleep {} seoncds to avoid being blocked by website".format(sleep_time))

def calculate_intrinsic_value(stocks):
    perpetualGrowthRate = 0.02 # Choose inflation rate.
    intrinsicValueCalculator = IntrinsicValueCalculator()
    for stock in stocks:
        if stock.m_intrinsic_value is None:
            if (stock.m_free_cash_flow_per_share 
                and stock.m_free_cash_flow_per_share_growth_rate 
                and stock.m_weighted_average_cost_of_capital_ratio):
                stock.m_intrinsic_value = intrinsicValueCalculator.calculateIntrinsicValueBasedOnDiscountedCashFlow(
                    stock.m_free_cash_flow_per_share,
                    stock.m_free_cash_flow_per_share_growth_rate,
                    stock.m_weighted_average_cost_of_capital_ratio,
                    perpetualGrowthRate
                )

def main(argv):
    argumentParser = argparse.ArgumentParser(description='Command list.')
    argumentParser.add_argument('-t','--tickers', nargs='+', help='StockPicker.py -t AAPL AMZN', required=False)
    argumentParser.add_argument('-tf','--tickers-file',  help='StockPicker.py -tf ./tickers.txt', required=False)
    args = argumentParser.parse_args()

    tickers = []
    if args.tickers:
        tickers = args.tickers
    elif args.tickers_file:
        print ("Getting tickers from file {}".format(args.tickers_file))
        with open(args.tickers_file) as file:
            lines = file.readlines()
            tickers = [line.rstrip() for line in lines]
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

    personal_strategy = PersonalStrategy()
    good_stocks = personal_strategy.recommend_good_stocks(stocks)
    print("{} of good stocks are recommended: ".format(str(len(good_stocks))))
    f = open("goodstocks.txt", "a")
    for stock in good_stocks:
        f.write(stock.to_json())
    f.close()
    exit(0)

if __name__ == "__main__":
    main(sys.argv)

