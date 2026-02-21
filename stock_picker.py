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
    
    # Define which fields need formatting
    dollar_fields = {'m_price', 'm_book_value_per_share', 'm_earnings_per_share', 
                     'm_market_cap', 'm_total_assets', 'm_total_liabilities',
                     'm_free_cash_flow_per_share', 'm_intrinsic_value_by_dcf',
                     'm_intrinsic_value_by_gurufocus'}
    
    percentage_fields = {'m_dividend_yield', 'm_profit_margin', 'm_return_on_equity',
                        'm_return_on_assets', 'm_return_on_capital', 
                        'm_weighted_average_cost_of_capital_ratio',
                        'm_price_to_book_ratio'}
    
    ratio_fields = {'m_current_ratio', 'm_debt_to_equity',
                   'm_price_to_earnings_ratio', 'm_peg_ratio',
                   'm_price_to_free_cash_flow_per_share', 'm_price_to_intrinsic_value_ratio'}
    
    def format_value(attribute, value):
        """Format value based on attribute type"""
        if value is None:
            return ''
        
        if attribute in dollar_fields:
            if attribute == 'm_market_cap' or attribute == 'm_total_assets' or attribute == 'm_total_liabilities':
                # Format large numbers in billions/millions
                if value >= 1_000_000_000:
                    return f"{value / 1_000_000_000:.2f} billion$"
                elif value >= 1_000_000:
                    return f"{value / 1_000_000:.2f} million$"
                else:
                    return f"{value:,.2f}$"
            else:
                return f"{value:.2f}$"
        elif attribute in percentage_fields:
            # Yahoo Finance returns values as-is (0.9 = 0.9%, not 90%)
            return f"{value:.2f}%"
        elif attribute in ratio_fields:
            return f"{value:.2f}"
        else:
            return value
    
    with open(csv_path, 'w',) as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(stock_attributes)
        for stock in stocks:
            row = []
            for attribute in stock_attributes:
                value = getattr(stock, attribute)
                formatted_value = format_value(attribute, value)
                row.append(formatted_value)
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
