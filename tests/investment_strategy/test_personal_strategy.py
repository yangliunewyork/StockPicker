"""Unit tests for PersonalStrategy"""
import unittest
from investment_strategy.personal_strategy import PersonalStrategy
from model.stock import Stock


class TestPersonalStrategy(unittest.TestCase):
    """Test cases for PersonalStrategy class"""

    def setUp(self):
        """Set up test fixtures"""
        self.strategy = PersonalStrategy()

    def create_stock(self, symbol, price, intrinsic_value, roe, debt_to_equity, peg, price_to_fcf):
        """Helper to create a stock with specific values"""
        stock = Stock()
        stock.m_symbol = symbol
        stock.m_price = price
        stock.m_intrinsic_value_by_gurufocus = intrinsic_value
        stock.m_return_on_equity = roe
        stock.m_debt_to_equity = debt_to_equity
        stock.m_peg_ratio = peg
        stock.m_price_to_free_cash_flow_per_share = price_to_fcf
        return stock

    def test_good_stock_passes_all_criteria(self):
        """Test that a good stock passes all criteria"""
        stock = self.create_stock(
            symbol="GOOD",
            price=100.0,
            intrinsic_value=150.0,
            roe=0.20,
            debt_to_equity=0.5,
            peg=2.0,
            price_to_fcf=20.0
        )
        
        result = self.strategy._is_good_stock(stock)
        self.assertTrue(result)
        self.assertAlmostEqual(stock.m_price_to_intrinsic_value_ratio, 100.0/150.0)

    def test_low_roe_fails(self):
        """Test that low ROE fails criteria"""
        stock = self.create_stock(
            symbol="LOWROE",
            price=100.0,
            intrinsic_value=150.0,
            roe=0.10,  # Below 0.15 threshold
            debt_to_equity=0.5,
            peg=2.0,
            price_to_fcf=20.0
        )
        
        result = self.strategy._is_good_stock(stock)
        self.assertFalse(result)

    def test_high_debt_fails(self):
        """Test that high debt-to-equity fails criteria"""
        stock = self.create_stock(
            symbol="HIGHDEBT",
            price=100.0,
            intrinsic_value=150.0,
            roe=0.20,
            debt_to_equity=1.5,  # Above 1.0 threshold
            peg=2.0,
            price_to_fcf=20.0
        )
        
        result = self.strategy._is_good_stock(stock)
        self.assertFalse(result)

    def test_high_peg_fails(self):
        """Test that high PEG ratio fails criteria"""
        stock = self.create_stock(
            symbol="HIGHPEG",
            price=100.0,
            intrinsic_value=150.0,
            roe=0.20,
            debt_to_equity=0.5,
            peg=4.0,  # Above 3.0 threshold
            price_to_fcf=20.0
        )
        
        result = self.strategy._is_good_stock(stock)
        self.assertFalse(result)

    def test_overvalued_stock_fails(self):
        """Test that overvalued stock fails criteria"""
        stock = self.create_stock(
            symbol="OVERVAL",
            price=300.0,
            intrinsic_value=100.0,  # Price is 3x intrinsic value
            roe=0.20,
            debt_to_equity=0.5,
            peg=2.0,
            price_to_fcf=20.0
        )
        
        result = self.strategy._is_good_stock(stock)
        self.assertFalse(result)

    def test_recommend_good_stocks_filters_and_sorts(self):
        """Test that recommend_good_stocks filters and sorts correctly"""
        stocks = [
            self.create_stock("GOOD1", 100.0, 200.0, 0.20, 0.5, 2.0, 20.0),
            self.create_stock("GOOD2", 150.0, 200.0, 0.20, 0.5, 2.0, 20.0),
            self.create_stock("BAD", 100.0, 50.0, 0.10, 2.0, 5.0, 40.0),
        ]
        
        good_stocks = self.strategy.recommend_good_stocks(stocks)
        
        self.assertEqual(len(good_stocks), 2)
        # Should be sorted by price-to-intrinsic-value ratio (ascending)
        self.assertEqual(good_stocks[0].m_symbol, "GOOD1")
        self.assertEqual(good_stocks[1].m_symbol, "GOOD2")

    def test_recommend_good_stocks_skips_missing_data(self):
        """Test that stocks with missing data are skipped"""
        stocks = [
            self.create_stock("GOOD", 100.0, 200.0, 0.20, 0.5, 2.0, 20.0),
        ]
        stocks[0].m_intrinsic_value_by_gurufocus = None
        
        good_stocks = self.strategy.recommend_good_stocks(stocks)
        
        self.assertEqual(len(good_stocks), 0)


if __name__ == '__main__':
    unittest.main()
