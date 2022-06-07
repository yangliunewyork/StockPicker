"""
DataCollectorManager is a class to manage data collectors, and provide API to
return information from these data collectors.
"""
from multiprocessing.dummy import Pool as ThreadPool

from data_collector.nasdaq_data_collector import NasdaqDataCollector
from data_collector.yahoo_finance_data_collector import YahooFinanceDataCollector
from data_collector.guru_focus_data_collector import GuruFocusDataCollector

class DataCollectorManager:
    """
    A class to manage data collectors, and provide API to return information
    from these data collectors.
    """

    _yahoo_finance_data_collector = YahooFinanceDataCollector()
    _guru_focus_data_collector = GuruFocusDataCollector()
    # Disable it as it has a rate limit that requires 30 seconds apart
    # stockAnalysisWebsiteDataCollector = StockAnalysisWebsiteDataCollector()

    def get_stock_tickers(self):
        """
        Returns:
            A list of stock tickers.
        """
        nasdaq_data_collector = NasdaqDataCollector()
        tickers = nasdaq_data_collector.get_tickers()
        print("Total stocks in Nasdaq: ", str(len(tickers)))
        return tickers

    def gather_stock_information(self, stocks):
        """
        Call different data collectors to popuplate Stock instances' fields.
        """
        tread_pool = ThreadPool(6)
        stocks = tread_pool.map(self._call_data_collectors_for_stock, stocks)

    def _call_data_collectors_for_stock(self, stock):
        """
        Call data collectors for the specified stock.
        Arguments:
            stock: A Stock instance.
        """
        # sleep_time = 0.1
        self._yahoo_finance_data_collector.get_stock_info(stock)
        self._guru_focus_data_collector.get_stock_info(stock)
        # time.sleep(sleep_time)
        # print ("Sleep {} seoncds to avoid being blocked by website".format(sleep_time))
