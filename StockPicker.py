#!/usr/bin/python

import sys
import argparse
from DataCollector.DataCollectorManager import DataCollectorManager

from Model.Stock import Stock
from DataCollector.NasdaqDataCollector import NasdaqDataCollector
from InvestmentStrategy.PersonalStrategy import PersonalStrategy
from Utils.IntrinsicValueCalculator import IntrinsicValueCalculator


def calculate_intrinsic_value(stocks):
    perpetualGrowthRate = 0.02  # Choose inflation rate.
    intrinsicValueCalculator = IntrinsicValueCalculator()
    for stock in stocks:
        if stock.m_intrinsic_value is None:
            if (
                stock.m_free_cash_flow_per_share
                and stock.m_free_cash_flow_per_share_growth_rate
                and stock.m_weighted_average_cost_of_capital_ratio
            ):
                stock.m_intrinsic_value = intrinsicValueCalculator.calculateIntrinsicValueBasedOnDiscountedCashFlow(
                    stock.m_free_cash_flow_per_share,
                    stock.m_free_cash_flow_per_share_growth_rate,
                    stock.m_weighted_average_cost_of_capital_ratio,
                    perpetualGrowthRate,
                )


def main(argv):
    argumentParser = argparse.ArgumentParser(description="Command list.")
    argumentParser.add_argument(
        "-t", "--tickers", nargs="+", help="StockPicker.py -t AAPL AMZN", required=False
    )
    argumentParser.add_argument(
        "-tf", "--tickers-file", help="StockPicker.py -tf ./tickers.txt", required=False
    )
    args = argumentParser.parse_args()

    dataCollectorManager = DataCollectorManager()

    tickers = []
    if args.tickers:
        tickers = args.tickers
    elif args.tickers_file:
        print("Getting tickers from file {}".format(args.tickers_file))
        with open(args.tickers_file) as file:
            lines = file.readlines()
            tickers = [line.rstrip() for line in lines]
    else:
        tickers = dataCollectorManager.get_stock_tickers()

    # Initialize a list of Stock instances with only m_symbol field value populated
    stocks = []
    for ticker in tickers:
        stock = Stock()
        stock.m_symbol = ticker
        stocks.append(stock)

    dataCollectorManager.gather_stock_information(stocks)

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
