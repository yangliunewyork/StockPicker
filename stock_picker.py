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
    perpetual_growth_rate = 0.02  # Choose inflation rate.
    intrinsic_value_calculator = IntrinsicValueCalculator()
    for stock in stocks:
        if stock.m_intrinsic_value is None:
            if (
                stock.m_free_cash_flow_per_share
                and stock.m_free_cash_flow_per_share_growth_rate
                and stock.m_weighted_average_cost_of_capital_ratio
            ):
                stock.m_intrinsic_value = intrinsic_value_calculator.calculate_intrinsic_value_based_on_discounted_cash_flow(
                    stock.m_free_cash_flow_per_share,
                    stock.m_free_cash_flow_per_share_growth_rate,
                    stock.m_weighted_average_cost_of_capital_ratio,
                    perpetual_growth_rate,
                )

def write_stocks_to_csv(stocks):
    import os
    stock_attributes = stocks[0].get_stock_attributes()
    csv_path = 'stocks.csv'
    with open(csv_path, 'w',) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(stock_attributes)
        for stock in stocks:
            row = []
            for attribute in stock_attributes:
                row.append(getattr(stock, attribute))
            writer.writerow(row)
    
    absolute_path = os.path.abspath(csv_path)
    print(f"\nStock data saved to: {absolute_path}")
    print(f"Total stocks written: {len(stocks)}")  


def main(argv):
    argument_parser = argparse.ArgumentParser(description="Command list.")
    argument_parser.add_argument(
        "-t", "--tickers", nargs="+", help="StockPicker.py -t AAPL AMZN", required=False
    )
    argument_parser.add_argument(
        "-tf", "--tickers-file", help="StockPicker.py -tf ./tickers.txt", required=False
    )
    args = argument_parser.parse_args()

    data_collector_manager = DataCollectorManager()

    tickers = []
    if args.tickers:
        tickers = args.tickers
    elif args.tickers_file:
        logging.info("Getting tickers from file {}".format(args.tickers_file))
        with open(args.tickers_file) as file:
            lines = file.readlines()
            tickers = [line.rstrip() for line in lines]
    else:
        tickers = data_collector_manager.get_stock_tickers()

    # Initialize a list of Stock instances with only m_symbol field value populated
    stocks = []
    for ticker in tickers:
        stock = Stock()
        stock.m_symbol = ticker
        stocks.append(stock)

    data_collector_manager.gather_stock_information(stocks)

    write_stocks_to_csv(stocks)

    exit(0)


if __name__ == "__main__":
    main(sys.argv)
