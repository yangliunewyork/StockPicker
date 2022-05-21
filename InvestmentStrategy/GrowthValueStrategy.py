#!/usr/bin/python

from StockInvestmentStrategy import StockInvestmentStrategy

class GrowthValueStrategy(StockInvestmentStrategy):
    """
    Strategy Overview
    The Growth/Value Investor strategy is based on the book "What Works on Wall Street" 
    by James P. O'Shaughnessy.In the book, O'Shaughnessy back-tested 44 years of stock market 
    data from the comprehensive Standard & Poor's Compustat database to find out which 
    strategies work and which don't. To the surprise of many, he concluded that price-to-earnings 
    ratios aren't the best indicator of a stock's value, and that small-company stocks, 
    contrary to popular wisdom, don't as a group have an edge on large-company stocks. 
    Based on his research, O'Shaughnessy developed two key investment strategies: "Cornerstone Growth" 
    and "Cornerstone Value", both of which are combined to form this strategy.
    """
    def market_cap_test(self, stock):
        """
        The Cornerstone Value Strategy looks for large, well known companies 
        whose market cap is greater than $1 billion.
        These companies exhibit solid and stable earnings.
        """
        return stock.m_market_cap > 1000000000

    def cash_flow_per_share_test(self, stock):
        """
        Companies with strong cash flow are typically the value oriented investments 
        that this strategy looks for. The company's cash flow per share must be
        greater than the mean of the market cash flow per share ($1.61).
        """
        return stock.m_cash_flow_per_share > 1.61

    def share_outstanding_test(self, stock):
        """
        This particular strategy looks for companies whose total number of outstanding 
        shares are in excess of the market average (632 million shares).
        """
        return stock.m_share_outstanding > 60000000

    def trailing_twelve_months_sales_test(self, stock):
        """
        A company's trailing 12 month sales ($30,390 million) are required 
        to be 1.5 times greater than the mean of the
        market's trailing 12 month sales ($20,973 million).
        """
        return stock.m_trailing_twelve_months_sales > 30390000000

    def dividend_test(self,stock):
        """
        The final step in the Cornerstone Value strategy is to select the 
        50 companies from the market leaders group (those that have passed the previous four criteria) 
        that have the highest dividend yield.
        """
        return stock.m_dividend_yield > 0 # At this moment, choose positive

    def stock_validation(self, stock):
        return cash_flow_per_share_test(stock)
        and share_outstanding_test(stock)
        and trailing_twelve_months_sales_test(stock)
        and dividend_test(stock)
