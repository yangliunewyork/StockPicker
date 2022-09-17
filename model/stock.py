"""
Stores stock information.
"""
import json

from model.stock_valuation_data import StockValuationData

class Stock:
    """
    Stores stock information.
    """

    def __init__(self):
        # Basics
        self.m_symbol = None
        self.m_book_value_per_share = None
        self.m_company_name = None
        self.m_price = None
        self.m_earnings_per_share = None
        self.m_dividend_yield = None
        self.m_market_cap = None
        self.m_share_outstading = None
        self.m_total_assets = None
        self.m_total_liabilities = None
        self.m_equity_per_share = None
        self.m_total_outstanding_shares = None
        self.m_free_cash_flow_per_share = None
        self.m_free_cash_flow_per_share_growth_rate = None
        # Health
        self.m_current_ratio = None
        self.m_debt_to_equity = None
        # Ratios
        self.m_profit_margin = None
        self.m_price_to_book_ratio = None
        self.m_price_to_earnings_ratio = None
        self.m_return_on_equity = None
        self.m_return_on_assets = None
        self.m_return_on_capital = None
        self.m_peg_ratio = None
        self.m_weighted_average_cost_of_capital_ratio = None
        self.m_price_to_free_cash_flow_per_share = None
        
        # Valuation data
        self.m_price_to_intrinsic_value_ratio = None
        self.m_valuation_data = StockValuationData()

    def to_json(self):
        """
        Serilization.
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
