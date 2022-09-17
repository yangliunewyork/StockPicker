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
        Return true if this is a good stock. Should give some margin for these metrics, and not give a tight limit.

        Arguments:
            stock: A Stock instance.
        Returns:
            True if this is a good stock. Otherwise returns False.
        """
        stock.m_price_to_intrinsic_value_ratio = stock.m_price / stock.m_valuation_data.m_intrinsic_value_by_gurufocus
        return (
            # How much profit a company can generate relative to shareholders’ equity
            stock.m_return_on_equity is not None
            and float(stock.m_return_on_equity) >= 0.15
            # How much debt a company has taken on relative to its equity
            and stock.m_debt_to_equity is not None
            and float(stock.m_debt_to_equity) <= 1
            #  Factoring in the company's growth rate to its PE ratio to check whether it is fair value 
            and stock.m_peg_ratio is not None
            and float(stock.m_peg_ratio) <= 2
            #  Check stock price against its intrinsic value(which we scrapped online or calculated by ourself)
            #  to make sure the price is fair. 
            and stock.m_price_to_intrinsic_value_ratio < 2
        )
