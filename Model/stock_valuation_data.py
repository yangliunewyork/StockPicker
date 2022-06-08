"""
Stores valuation for a stock.
"""
import json


class StockValuationData:
    """
    Stores stock information.
    """

    def __init__(self):
        # Basics
        self.m_symbol = None
        self.m_price = None
        self.m_intrinsic_value = None

    def to_json(self):
        """
        Serilization.
        """
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
