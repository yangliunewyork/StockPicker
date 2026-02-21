"""
DataCollectorManager is a class to manage data collectors, and provide API to
return information from these data collectors.
"""
from multiprocessing.dummy import Pool as ThreadPool
import numpy
from alive_progress import alive_it

from data_collector.nasdaq_data_collector import NasdaqDataCollector
from data_collector.yahoo_finance_data_collector import YahooFinanceDataCollector
from model.stock import Stock


class DataCollectorManager:
    """
    A class to manage data collectors, and provide API to return information
    from these data collectors.
    """

    _yahoo_finance_data_collector = YahooFinanceDataCollector()
    # Disabled GuruFocus collector due to 403 blocking issues
    # Disabled StockAnalysisWebsite collector due to rate limit (requires 30 seconds apart)

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
        # tread_pool = ThreadPool(6)
        # stocks = tread_pool.map(self._call_data_collectors_for_stock, stocks)
        for stock in alive_it(stocks):
            self._call_data_collectors_for_stock(stock)

    def _call_data_collectors_for_stock(self, stock):
        """
        Call data collectors for the specified stock.
        Arguments:
            stock: A Stock instance.
        """
        self._yahoo_finance_data_collector.get_stock_info(stock)


if __name__ == "__main__":
    data_collector_manager = DataCollectorManager()
    evr_stock = Stock()
    evr_stock.m_symbol = "EVR"
    stocks = []
    stocks.append(evr_stock)
    data_collector_manager.gather_stock_information(stocks)
    for stock in stocks:
        print(stock.to_json())
