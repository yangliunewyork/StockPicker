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
        self.get_intrinsic_value(stock)

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

    def get_intrinsic_value(self, stock):
        self.get_intrinsic_value_for_nasdaq_stock(stock)
        if (stock.m_intrinsic_value is None or stock.m_intrinsic_value == 0): # This may be a NYSE stock
            self.get_intrinsic_value_for_nyse_stock(stock)

    def get_intrinsic_value_for_nasdaq_stock(self, stock):
        url = "https://www.gurufocus.com/term/iv_dcf_share/NAS:{}/Price-to-Projected-FCF/".format(stock.m_symbol)
        self.scraping_intrinsic_value(stock, url)

    def get_intrinsic_value_for_nyse_stock(self, stock):
        url = "https://www.gurufocus.com/term/iv_dcf/NYSE:{}/Intrinsic-Value".format(stock.m_symbol)
        self.scraping_intrinsic_value(stock, url)

    def scraping_intrinsic_value(self, stock, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print (response.status_code)
        parser = html.fromstring(response.content)
        innter_text = parser.xpath('//div[@id="def_body_detail_height"]/font')[0].text_content()
        match = re.search(r'\d{1,3}(,\d{3})*(\.\d+)?', innter_text)
        if match :
            intrinsic_value_str = match.group(0).replace(",","")
            #print (intrinsic_value_str)
            stock.m_intrinsic_value = float(intrinsic_value_str)
            if stock.m_intrinsic_value == 0: # The default value is 0 for this website
                stock.m_intrinsic_value = None
        else:
            print("Intrinsic value is not found for stock {}".format(stock.m_symbol))



if __name__ == "__main__":
    dataCollector = GuruFocusDataCollector()
    stock = Stock()
    stock.m_symbol = 'GOOGL'
    dataCollector.get_stock_info(stock)
    print(stock.to_json())
    stock.m_symbol = 'SQ'
    dataCollector.get_stock_info(stock)
    print(stock.to_json())
