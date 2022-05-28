#!/usr/bin/python

from InvestmentStrategy.StockInvestmentStrategy import StockInvestmentStrategy


class PersonalStrategy(StockInvestmentStrategy):
    """
    My personal investment strategy
    """

    def recommend_good_stocks(self, stocks):
        good_stocks = []
        for stock in stocks:
            if (stock.m_intrinsic_value is None or stock.m_price is None):
                continue
            if self.is_good_stock(stock):
                good_stocks.append(stock)

        # Sorting and printing
        good_stocks.sort(key=lambda x: (x.m_price_to_intrinsic_value_ratio), reverse=False)
        return good_stocks


    def is_good_stock(self, stock):
        if (stock.m_intrinsic_value is None or stock.m_price is None):
            return False
        stock.m_price_to_intrinsic_value_ratio = stock.m_price / stock.m_intrinsic_value
        return (stock.m_price_to_book_ratio != None
                and float(stock.m_price_to_book_ratio) <= 10
                and stock.m_return_on_equity != None
                and float(stock.m_return_on_equity) >= 0.15
                and stock.m_price_to_intrinsic_value_ratio < 3)
