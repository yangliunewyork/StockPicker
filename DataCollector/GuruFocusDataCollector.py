#!/usr/bin/python

from lxml import html
from Model.Stock import Stock
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class GuruFocusDataCollector:
    """                                                                                                 
    A class to pull information from https://www.gurufocus.com/                                                      
    """

    def get_stock_info(self, stock):
        self.get_stock_info_from_cash_flow_statement(stock)
        self.get_stock_info_from_ratios(stock)

    def get_wacc(self, stock):
        url = "https://www.gurufocus.com/term/wacc/NAS:{}/WACC".format(stock.m_symbol)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print (response.status_code)
        parser = html.fromstring(response.content)
        ratios_table = parser.xpath('//div[@id="def_body_detail_height"]')[0]
        print (ratios_table)

if __name__ == "__main__":
    dataCollector = GuruFocusDataCollector()
    stock = Stock()
    stock.m_symbol = 'AMZN'
    data = dataCollector.get_stock_info()
    for symbol in data:
        print(data[symbol].to_json())
