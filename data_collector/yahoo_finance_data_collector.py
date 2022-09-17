"""
YahooFinanceDataCollector is a class to collect information from Yahoo finance API.
"""
import yfinance as yf

from model.stock import Stock


class YahooFinanceDataCollector:
    """
    A class to pull information from Yahoo Finance
    """

    # pylint: disable=R0201
    def get_stock_info(self, stock):
        """
        Return a list of stock information.
        """
        print(f"Getting stock information for {stock.m_symbol} ...")
        # yahoostock_info = Share(symbol)
        stock_info = yf.Ticker(stock.m_symbol)
        # print (stock_info.info)
        if "shortName" in stock_info.info:
            stock.m_company_name = stock_info.info["shortName"]
        if "currentPrice" in stock_info.info:
            stock.m_price = stock_info.info["currentPrice"]
        if "bookValue" in stock_info.info:
            stock.m_book_value_per_share = stock_info.info["bookValue"]
        if "priceToBook" in stock_info.info:
            stock.m_price_to_book_ratio = stock_info.info["priceToBook"]
        if "dividendYield" in stock_info.info:
            stock.m_dividend_yield = stock_info.info["dividendYield"]
        if "totalCashPerShare" in stock_info.info:
            stock.m_cash_per_share = stock_info.info["totalCashPerShare"]
        if "profitMargins" in stock_info.info:
            stock.m_profit_margin = stock_info.info["profitMargins"]
        if "currentRatio" in stock_info.info:
            stock.m_current_ratio = stock_info.info["currentRatio"]
        if (
            "debtToEquity" in stock_info.info
            and stock_info.info["debtToEquity"] is not None
        ):
            stock.m_debt_to_equity = stock_info.info["debtToEquity"] / 100
        if "marketCap" in stock_info.info:
            stock.m_market_cap = stock_info.info["marketCap"]
        if "returnOnAssets" in stock_info.info:
            stock.m_return_on_assets = stock_info.info["returnOnAssets"]
        if "returnOnEquity" in stock_info.info:
            stock.m_return_on_equity = stock_info.info["returnOnEquity"]
        if "pegRatio" in stock_info.info:
            stock.m_peg_ratio = stock_info.info["pegRatio"]


if __name__ == "__main__":
    dataCollector = YahooFinanceDataCollector()
    amazon_stock = Stock()
    amazon_stock.m_symbol = "BA"
    dataCollector.get_stock_info(amazon_stock)
    print(amazon_stock.to_json())
