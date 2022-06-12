"""
GuruFocusDataCollector is a class to collect information from https://www.gurufocus.com/.
"""
import traceback
import logging
import re
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from lxml import html

from model.stock import Stock

class GuruFocusDataCollector:
    """
    A class to pull information from https://www.gurufocus.com/
    """

    REQUEST_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)"
        "AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/50.0.2661.102"
        "Safari/537.36"
    }

    def get_stock_info(self, stock):
        """
        Get stock information from https://www.gurufocus.com/.

        Arguments:
            stock: A Stock instance.
        """
        try:
            self._get_wacc(stock)
        except Exception:
            logging.warning(traceback.format_exc())
        try:
            self._get_intrinsic_value_based_on_discounted_cash_flow(stock)
        except Exception:
            logging.warning(traceback.format_exc())

    def _get_wacc(self, stock):
        """
        Scraping WACC value.

        Arguments:
            stock: A Stock instance.
        """
        url = f"https://www.gurufocus.com/term/wacc/NAS:{stock.m_symbol}/WACC"
        response = requests.get(url, headers=self.REQUEST_HEADERS)
        if response.status_code != 200:
            print(response.status_code)
        parser = html.fromstring(response.content)
        innter_text = parser.xpath('//div[@id="def_body_detail_height"]/font')[
            0
        ].text_content()
        # print (innter_text)
        match = re.search(r"(\d+(\.\d+)?%)", innter_text)
        if match:
            wacc_ratio_str = match.group(0)
            wacc_ratio = float(wacc_ratio_str.strip("%")) / 100
            stock.m_weighted_average_cost_of_capital_ratio = wacc_ratio
        # else:
        # print("WACC ratio is not found for stock {}".format(stock.m_symbol))

    def _get_intrinsic_value_based_on_discounted_cash_flow(self, stock):
        """
        Scraping intrinsic value.

        Arguments:
            stock: A Stock instance.
        """
        self._scraping_intrinsic_value(stock)

    def _scraping_intrinsic_value(self, stock):
        url = f"https://www.gurufocus.com/term/iv_dcf/{stock.m_symbol}/Intrinsic-Value-DCF-FCF-Based/"
        response = requests.get(url, headers=self.REQUEST_HEADERS)
        if response.status_code != 200:
            print(response.status_code)
        parser = html.fromstring(response.content)
        innter_text = parser.xpath('//div[@id="def_body_detail_height"]/font')[
            0
        ].text_content()
        match = re.search(r"\d{1,3}(,\d{3})*(\.\d+)?", innter_text)
        if match:
            intrinsic_value_str = match.group(0).replace(",", "")
            # print (intrinsic_value_str)
            stock.m_valuation_data.m_intrinsic_value_by_gurufocus = float(intrinsic_value_str)
            if stock.m_valuation_data.m_intrinsic_value_by_gurufocus == 0:  # The default value is 0 for this website
                stock.m_valuation_data.m_intrinsic_value_by_gurufocus = None


if __name__ == "__main__":
    dataCollector = GuruFocusDataCollector()
    google_stock = Stock()
    google_stock.m_symbol = "GOOGL"
    dataCollector.get_stock_info(google_stock)
    print(google_stock.to_json())
    square_stock = Stock()
    square_stock.m_symbol = "SQ"
    dataCollector.get_stock_info(square_stock)
    print(square_stock.to_json())
    evr_stock = Stock()
    evr_stock.m_symbol = "EVR"
    dataCollector.get_stock_info(evr_stock)
    print(evr_stock.to_json())
