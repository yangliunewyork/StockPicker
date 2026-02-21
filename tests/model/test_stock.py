"""Unit tests for Stock model"""
import unittest
import json
from model.stock import Stock


class TestStock(unittest.TestCase):
    """Test cases for Stock class"""

    def setUp(self):
        """Set up test fixtures"""
        self.stock = Stock()

    def test_stock_initialization(self):
        """Test that Stock initializes with None values"""
        self.assertIsNone(self.stock.m_symbol)
        self.assertIsNone(self.stock.m_price)
        self.assertIsNone(self.stock.m_company_name)

    def test_stock_attributes_assignment(self):
        """Test assigning values to stock attributes"""
        self.stock.m_symbol = "AAPL"
        self.stock.m_price = 150.0
        self.stock.m_company_name = "Apple Inc."
        
        self.assertEqual(self.stock.m_symbol, "AAPL")
        self.assertEqual(self.stock.m_price, 150.0)
        self.assertEqual(self.stock.m_company_name, "Apple Inc.")

    def test_get_stock_attributes(self):
        """Test getting list of stock attributes"""
        attributes = self.stock.get_stock_attributes()
        
        self.assertIsInstance(attributes, list)
        self.assertIn('m_symbol', attributes)
        self.assertIn('m_price', attributes)
        self.assertIn('m_book_value_per_share', attributes)
        self.assertGreater(len(attributes), 0)

    def test_to_json(self):
        """Test JSON serialization"""
        self.stock.m_symbol = "TSLA"
        self.stock.m_price = 200.0
        
        json_str = self.stock.to_json()
        self.assertIsInstance(json_str, str)
        
        # Verify it's valid JSON
        data = json.loads(json_str)
        self.assertEqual(data['m_symbol'], "TSLA")
        self.assertEqual(data['m_price'], 200.0)


if __name__ == '__main__':
    unittest.main()
