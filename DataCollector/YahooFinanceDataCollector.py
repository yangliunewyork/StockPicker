#!/usr/bin/python
import requests
import csv
from Model.Stock import Stock
import yfinance as yf
import pandas as pd

class YahooFinanceUrlBuilder:
    """
    @ToBeDeprecated
    Build Yahoo Finance API url.
    """

    def __init__(self):
        self.yahoo_url = "http://finance.yahoo.com/d/quotes.csv?"

    def add_symbols(self, symbols):
        """
        Add comma-seprated symbols to url.
        """
        self.yahoo_url += "s=" + symbols
        return self

    def add_fields(self, fields):
        """
        Add comma-separated fields to url.
        """
        # API fields don't need seperator
        fields = fields.replace(',', '')
        self.yahoo_url += "&f=" + fields
        return self

    def get_url(self):
        """
        Return the constructed url.
        """
        return self.yahoo_url


class YahooFinanceDataCollector:
    """                                                                                                 
    A class to pull information from Yahoo Finance                                                        
    """

    def get_data(self, yahoo_url):
        """
        Return the information we get from Yahoo Finance API.
        """
        resp = requests.get(yahoo_url)
        text = resp.iter_lines()
        reader = csv.reader(text, delimiter=',')
        data = []
        for row in reader:
            data.append(row)
        return data

    def get_stock_info(self, stock):
        """
        Return a list of stock information.
        """
        print("Getting stock information for {} ...".format(stock.m_symbol))
        #yahooStockInfo = Share(symbol)
        stockInfo = yf.Ticker(stock.m_symbol)
        
        if 'bookValue' in stockInfo.info:
            stock.m_book_value_per_share = stockInfo.info['bookValue']
        if 'priceToBook' in stockInfo.info:
            stock.m_price_to_book_ratio = stockInfo.info['priceToBook']
        if 'dividendYield' in stockInfo.info:
            stock.m_dividend_yield = stockInfo.info['dividendYield']
        if 'totalCashPerShare' in stockInfo.info:
            stock.m_cash_per_share = stockInfo.info['totalCashPerShare']
        if 'marketCap' in stockInfo.info:
            stock.m_market_cap = stockInfo.info['marketCap']
        if 'returnOnEquity' in stockInfo.info:
            stock.m_return_on_equity_ratio = stockInfo.info['returnOnEquity']
        if 'freeCashflow' in stockInfo.info and 'sharesOutstanding' in stockInfo.info:
            stock.m_cash_flow_per_share = stockInfo.info['freeCashflow'] / stockInfo.info['sharesOutstanding']


if __name__ == "__main__":
    dataCollector = YahooFinanceDataCollector()
    data = dataCollector.get_stock_info(["GOOG", "FB"])
    for symbol in data:
        print(data[symbol].to_json())
