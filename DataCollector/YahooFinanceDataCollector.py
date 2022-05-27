#!/usr/bin/python
import requests
import csv
import yfinance as yf
import pandas as pd

from Model.Stock import Stock

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
        #print (stockInfo.info)
        if 'shortName' in stockInfo.info:
            stock.m_company_name = stockInfo.info['shortName']
        if 'currentPrice' in stockInfo.info:
            stock.m_price = stockInfo.info['currentPrice']
        if 'bookValue' in stockInfo.info:
            stock.m_book_value_per_share = stockInfo.info['bookValue']
        if 'priceToBook' in stockInfo.info:
            stock.m_price_to_book_ratio = stockInfo.info['priceToBook']
        if 'dividendYield' in stockInfo.info:
            stock.m_dividend_yield = stockInfo.info['dividendYield']
        if 'totalCashPerShare' in stockInfo.info:
            stock.m_cash_per_share = stockInfo.info['totalCashPerShare']
        if 'profitMargins' in stockInfo.info:
            stock.m_profit_margin = stockInfo.info['profitMargins']    
        if 'marketCap' in stockInfo.info:
            stock.m_market_cap = stockInfo.info['marketCap']
        if 'returnOnAssets' in stockInfo.info:
            stock.m_return_on_assets = stockInfo.info['returnOnAssets']
        if 'returnOnEquity' in stockInfo.info:
            stock.m_return_on_equity_ratio = stockInfo.info['returnOnEquity']
        if 'pegRatio' in stockInfo.info:
            stock.m_peg_ratio = stockInfo.info['pegRatio']
        if 'freeCashflow' in stockInfo.info and 'sharesOutstanding' in stockInfo.info:
            stock.m_cash_flow_per_share = stockInfo.info['freeCashflow'] / stockInfo.info['sharesOutstanding']


if __name__ == "__main__":
    dataCollector = YahooFinanceDataCollector()
    stock = Stock()
    stock.m_symbol = 'AMZN'
    dataCollector.get_stock_info(stock)
    print(stock.to_json())
