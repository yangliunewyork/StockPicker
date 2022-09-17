"""
GuruFocusDataCollector is a class to collect information from https://stockanalysis.com/.
"""
from lxml import html
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from model.stock import Stock


class StockAnalysisWebsiteDataCollector:
    """
    A class to pull information from https://stockanalysis.com/
    """

    REQUEST_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/50.0.2661.102"
        "Safari/537.36"
    }

    def get_stock_info(self, stock):
        """
        Arguments:
            stock: An instance of Stock class that stores stock information.
        """
        self.get_stock_info_from_cash_flow_statement(stock)
        self.get_stock_info_from_ratios(stock)

    def get_latest_value_for_ratio_from_ratios_table(self, ratios_table, ratio_name):
        """
        Return the extracted ratio value from the web component.

        Arguments:
            ratios_table: Represents a component that contains the ratios table
                in the webpage's HTML object.
            ratio_name: Represents the name of the ratio that we want to extract
                from the ratios_table component.
        Returns:
            A float number that represents the extracted ratio value.
        """
        ratio_value = ratios_table.xpath(
            f'//tr[td/span/text()[contains(., "{ratio_name}")]]'
        )[0].xpath(".//td/span/text()")[1:][0]
        return float(ratio_value.strip("%")) / 100

    def get_stock_info_from_ratios(self, stock):
        """
        Populate stock's ratio related fields.

        Arguments:
            stock: An instance of Stock class that stores stock information.
        """
        url = f"https://stockanalysis.com/stocks/{stock.m_symbol}/financials/ratios"
        response = requests.get(url, headers=self.REQUEST_HEADERS)
        if response.status_code != 200:
            print(response.status_code)
        parser = html.fromstring(response.content)
        ratios_table = parser.xpath('//table[@id="financial-table"]')[0]

        if not stock.m_price_to_earnings_ratio:
            stock.m_price_to_earnings_ratio = (
                self.get_latest_value_for_ratio_from_ratios_table(
                    ratios_table, "PE Ratio"
                )
            )
        if not stock.m_price_to_earnings_ratio:
            stock.m_price_to_earnings_ratio = (
                self.get_latest_value_for_ratio_from_ratios_table(
                    ratios_table, "PE Ratio"
                )
            )
        if not stock.m_return_on_equity:
            stock.m_return_on_equity = (
                self.get_latest_value_for_ratio_from_ratios_table(
                    ratios_table, "Return on Equity (ROE)"
                )
            )
        if not stock.m_return_on_assets:
            stock.m_return_on_assets = (
                self.get_latest_value_for_ratio_from_ratios_table(
                    ratios_table, "Return on Assets (ROA)"
                )
            )
        if not stock.m_return_on_capital:
            stock.m_return_on_capital = (
                self.get_latest_value_for_ratio_from_ratios_table(
                    ratios_table, "Return on Capital (ROIC)"
                )
            )

    def get_stock_info_from_cash_flow_statement(self, stock):
        """
        Get stock information from cash flow statement.
        Arguments:
            stock: An instance of Stock class that stores stock information.
        """
        url = f"https://stockanalysis.com/stocks/{stock.m_symbol}/financials/cash-flow-statement"
        response = requests.get(url, headers=self.REQUEST_HEADERS)
        parser = html.fromstring(response.content)
        # print (html.tostring(parser))
        # print (parser.xpath('//table[@id="financial-table"]'))
        cash_flow_statement_table = parser.xpath('//table[@id="financial-table"]')[0]

        if not stock.m_free_cash_flow_per_share:
            stock.m_free_cash_flow_per_share = float(
                cash_flow_statement_table.xpath(
                    '//tr[td/span/text()[contains(., "Free Cash Flow Per Share")]]'
                )[0].xpath(".//td/span/text()")[1:][0]
            )

        if not stock.m_free_cash_flow_per_share_growth_rate:
            growth_rate_list = cash_flow_statement_table.xpath(
                '//tr[td/span/text()[contains(., "Free Cash Flow Growth")]]'
            )[0].xpath(".//td/span/text()")[1:]
            # print (growth_rate_list)
            float_growth_rate_list = []
            for item in growth_rate_list:
                float_growth_rate_list.append(float(item.strip("%")) / 100)
            # print(float_growth_rate_list)
            average_growth_rate = sum(float_growth_rate_list) / len(
                float_growth_rate_list
            )
            stock.m_free_cash_flow_per_share_growth_rate = average_growth_rate


if __name__ == "__main__":
    dataCollector = StockAnalysisWebsiteDataCollector()
    google_stock = Stock()
    google_stock.m_symbol = "GOOGL"
    dataCollector.get_stock_info(google_stock)
    print(google_stock.to_json())
