"""
This is a personal investment strategy that can be modified to suit your
personal investment purposes.
"""

from investment_strategy.stock_investment_strategy import StockInvestmentStrategy


class PersonalStrategy(StockInvestmentStrategy):
    """
    Personal investment strategy.
    """

    def recommend_good_stocks(self, stocks):
        """
        Return good stocks given the provided stock list.

        Arguments:
            stocks: A list of Stock instances.
        Returns:
            A list of good Stock instances.
        """
        good_stocks = []
        for stock in stocks:
            if stock.m_valuation_data.m_intrinsic_value_by_gurufocus is None or stock.m_price is None:
                print (stock.m_valuation_data.m_intrinsic_value_by_gurufocus)
                continue
            if self._is_good_stock(stock):
                good_stocks.append(stock)

        # Sorting and printing
        good_stocks.sort(
            key=lambda x: (x.m_price_to_intrinsic_value_ratio), reverse=False
        )
        return good_stocks

    def _is_good_stock(self, stock):
        """
        Return true if this is a good stock.

        Arguments:
            stock: A Stock instance.
        Returns:
            True if this is a good stock. Otherwise returns False.
        """
        stock.m_price_to_intrinsic_value_ratio = stock.m_price / stock.m_valuation_data.m_intrinsic_value_by_gurufocus
        return (
            stock.m_price_to_book_ratio is not None
            and float(stock.m_price_to_book_ratio) <= 10
            and stock.m_return_on_equity is not None
            and float(stock.m_return_on_equity) >= 0.15
            and stock.m_debt_to_equity is not None
            and float(stock.m_debt_to_equity) <= 2
            and stock.m_price_to_intrinsic_value_ratio < 2
        )
