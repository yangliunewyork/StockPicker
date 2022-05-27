#!/usr/bin/python

from lxml import html
import requests
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from Model.Stock import Stock

class GuruFocusDataCollector:
    """                                                                                                 
    A class to pull information from https://www.gurufocus.com/                                                      
    """

    def get_stock_info(self, stock):
        self.get_wacc(stock)

    def get_wacc(self, stock):
        url = "https://www.gurufocus.com/term/wacc/NAS:{}/WACC".format(stock.m_symbol)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print (response.status_code)
        parser = html.fromstring(response.content)
        innter_text = parser.xpath('//div[@id="def_body_detail_height"]/font')[0].text_content()
        #print (innter_text)
        match = re.search(r'(\d+(\.\d+)?%)', innter_text)
        if match :
            wacc_ratio_str = match.group(0)
            wacc_ratio = float(wacc_ratio_str.strip('%'))/100
            stock.m_weighted_average_cost_of_capital_ratio = wacc_ratio
        else:
            print("WACC ratio is not found for stock {}".format(stock.m_symbol))


if __name__ == "__main__":
    dataCollector = GuruFocusDataCollector()
    stock = Stock()
    stock.m_symbol = 'AMZN'
    dataCollector.get_stock_info(stock)
    print(stock.to_json())
