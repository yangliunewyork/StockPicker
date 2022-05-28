#!/usr/bin/python
from lxml import html
import csv
import pandas as pd
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from Model.Stock import Stock

class StockAnalysisWebsiteDataCollector:
    """                                                                                                 
    A class to pull information from https://stockanalysis.com/                                                       
    """

    def get_stock_info(self, stock):
        self.get_stock_info_from_cash_flow_statement(stock)
        self.get_stock_info_from_ratios(stock)

    def get_latest_value_for_ratio_from_ratios_table(self, ratios_table, ratio_name):
        ratio_value = ratios_table.xpath('//tr[td/span/text()[contains(., "{}")]]'.format(ratio_name))[0].xpath('.//td/span/text()')[1:][0]
        return float(ratio_value.strip('%'))/100

    def get_stock_info_from_ratios(self, stock):
        """
        Get stock information from ratios page
        """
        url = "https://stockanalysis.com/stocks/{}/financials/ratios".format(stock.m_symbol)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print (response.status_code)
        parser = html.fromstring(response.content)
        ratios_table = parser.xpath('//table[@id="financial-table"]')[0]

        if not stock.m_price_to_earnings_ratio:
            stock.m_price_to_earnings_ratio =  self.get_latest_value_for_ratio_from_ratios_table(ratios_table, "PE Ratio")
        if not stock.m_price_to_earnings_ratio:
            stock.m_price_to_earnings_ratio =  self.get_latest_value_for_ratio_from_ratios_table(ratios_table, "PE Ratio")
        if not stock.m_return_on_equity:
            stock.m_return_on_equity = self.get_latest_value_for_ratio_from_ratios_table(ratios_table, "Return on Equity (ROE)")
        if not stock.m_return_on_assets:
            stock.m_return_on_assets = self.get_latest_value_for_ratio_from_ratios_table(ratios_table, "Return on Assets (ROA)")
        if not stock.m_return_on_capital:
            stock.m_return_on_capital = self.get_latest_value_for_ratio_from_ratios_table(ratios_table, "Return on Capital (ROIC)")
        
    def get_stock_info_from_cash_flow_statement(self, stock):
        """
        Get stock information from cash flow statement.
        """
        url = "https://stockanalysis.com/stocks/{}/financials/cash-flow-statement".format(stock.m_symbol)
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        response = requests.get(url, headers=headers)
        parser = html.fromstring(response.content)
        #print (html.tostring(parser))
       # print (parser.xpath('//table[@id="financial-table"]'))
        cash_flow_statement_table = parser.xpath('//table[@id="financial-table"]')[0]

        if not stock.m_free_cash_flow_per_share:
            stock.m_free_cash_flow_per_share = float(cash_flow_statement_table.xpath('//tr[td/span/text()[contains(., "Free Cash Flow Per Share")]]')[0].xpath('.//td/span/text()')[1:][0])
        
        if not stock.m_free_cash_flow_per_share_growth_rate:
            growth_rate_list = cash_flow_statement_table.xpath('//tr[td/span/text()[contains(., "Free Cash Flow Growth")]]')[0].xpath('.//td/span/text()')[1:]
            #print (growth_rate_list)            
            float_growth_rate_list = []
            for item in growth_rate_list:
                float_growth_rate_list.append(float(item.strip('%'))/100)
            #print(float_growth_rate_list)
            average_growth_rate = sum(float_growth_rate_list) / len(float_growth_rate_list)
            stock.m_free_cash_flow_per_share_growth_rate = average_growth_rate


if __name__ == "__main__":
    dataCollector = StockAnalysisWebsiteDataCollector()
    stock = Stock()
    stock.m_symbol = 'GOOGL'
    dataCollector.get_stock_info(stock)
    print(stock.to_json())
