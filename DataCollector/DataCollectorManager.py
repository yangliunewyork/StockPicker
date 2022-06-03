import time
from multiprocessing.dummy import Pool as ThreadPool

from DataCollector.NasdaqDataCollector import NasdaqDataCollector
from DataCollector.YahooFinanceDataCollector import YahooFinanceDataCollector
from DataCollector.StockAnalysisWebsiteDataCollector import (
    StockAnalysisWebsiteDataCollector,
)
from DataCollector.GuruFocusDataCollector import GuruFocusDataCollector


class DataCollectorManager:
    """
    A class to manage data collection
    """

    yahooFinanceDataCollector = YahooFinanceDataCollector()
    guruFocusDataCollector = GuruFocusDataCollector()
    # Disable it as it has a rate limit that requires 30 seconds apart
    # stockAnalysisWebsiteDataCollector = StockAnalysisWebsiteDataCollector()

    def get_stock_tickers(self):
        """
        Returns:
            A list of stock tickers.
        """
        nasdaqDataCollector = NasdaqDataCollector()
        tickers = nasdaqDataCollector.get_tickers()
        print("Total stocks in Nasdaq: ", str(len(tickers)))
        return tickers

    def gather_stock_information(self, stocks):
        """
        Call different data collectors to popuplate Stock instances' fields.
        """
        treadPool = ThreadPool(6)
        stocks = treadPool.map(self.call_data_collectors_for_stock, stocks)

    def call_data_collectors_for_stock(self, stock):
        # sleep_time = 0.1
        self.yahooFinanceDataCollector.get_stock_info(stock)
        self.guruFocusDataCollector.get_stock_info(stock)
        # time.sleep(sleep_time)
        # print ("Sleep {} seoncds to avoid being blocked by website".format(sleep_time))
