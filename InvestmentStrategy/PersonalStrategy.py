#!/usr/bin/python

from InvestmentStrategy.StockInvestmentStrategy import StockInvestmentStrategy


class PersonalStrategy(StockInvestmentStrategy):
    """
    My personal investment strategy
    """

    def stock_validation(self, stock):
        return (stock.m_price_to_book_ratio != None
                and float(stock.m_price_to_book_ratio) <= 10
                and stock.m_return_on_equity != None
                and float(stock.m_return_on_equity) >= 0.15)
