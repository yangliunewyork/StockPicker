#!/usr/bin/python

import sys
import argparse
import logging
import csv

from data_collector.data_collector_manager import DataCollectorManager
from model.stock import Stock
from data_collector.nasdaq_data_collector import NasdaqDataCollector
from investment_strategy.personal_strategy import PersonalStrategy
from utils.intrinsic_value_calculator import IntrinsicValueCalculator


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

def write_stocks_to_csv(stocks):
    stock_attributes = stocks[0].get_stock_attributes()
    with open('stocks.csv', 'w',) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(stock_attributes)
        for stock in stocks:
            row = []
            for attribute in stock_attributes:
                row.append(getattr(stock, attribute))
            writer.writerow(row)  


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
        logging.info("Getting tickers from file {}".format(args.tickers_file))
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

    write_stocks_to_csv(stocks)

    exit(0)


if __name__ == "__main__":
    main(sys.argv)
