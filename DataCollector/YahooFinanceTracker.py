#!/usr/bin/python
import requests
import csv
from Model.Stock import Stock
#from yahoo_finance import Share # not working any more
import yfinance as yf
import pandas as pd


class YahooFinanceUrlBuilder:
    """
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


class YahooFinanceTracker:
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

    def get_data_from_yahoo(self, symbols_list):
        """
        Return a Dictionary of <symbol, Stock>
        Send request to Yahoo API in bulk.
        s : symbol
        e: Earnings per Share
        r: P/E Ratio
        r2: P/E Ratio (Realtime)
        r5: PEG Ratio
        y: Dividend Yield
        j1 : market cap
        j2: Shares Outstanding
        
        """
        stocks = []

        for symbol in symbols_list:
            print("Getting stock information for {} ...".format(symbol))
            #yahooStockInfo = Share(symbol)
            stock = Stock()
            stock.m_symbol = symbol
            stockInfo = yf.Ticker(symbol)
            #print(stockInfo.balancesheet)

            if 'bookValue' in stockInfo.info:
                #print(stockInfo.info['bookValue'])
                stock.m_book_value = stockInfo.info['bookValue']
            else:
                continue

            if 'priceToBook' in stockInfo.info:
                #print(stockInfo.info['bookValue'])
                stock.m_price_to_book_ratio = stockInfo.info['priceToBook']
            else:
                continue

            if 'dividendYield' in stockInfo.info:
                #print(stockInfo.info['bookValue'])
                stock.m_dividend_yield = stockInfo.info['dividendYield']
            if 'totalCashPerShare' in stockInfo.info:
                #print(stockInfo.info['bookValue'])
                stock.m_cash_per_share = stockInfo.info['totalCashPerShare']
            if 'marketCap' in stockInfo.info:
                #print(stockInfo.info['bookValue'])
                stock.m_market_cap = stockInfo.info['marketCap']
            if 'returnOnEquity' in stockInfo.info:
                #print(stockInfo.info['bookValue'])
                stock.m_return_on_equity = stockInfo.info['returnOnEquity']
            stocks.append(stock)
        return stocks


if __name__ == "__main__":
    tracker = YahooFinanceTracker()
    data = tracker.get_data_from_yahoo(["GOOG", "FB", "GILD", "AAPL"])
    for symbol in data:
        print(data[symbol].to_json())
