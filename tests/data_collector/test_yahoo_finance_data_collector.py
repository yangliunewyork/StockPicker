"""Unit tests for YahooFinanceDataCollector"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from data_collector.yahoo_finance_data_collector import YahooFinanceDataCollector
from model.stock import Stock


class TestYahooFinanceDataCollector(unittest.TestCase):
    """Test cases for YahooFinanceDataCollector class"""

    def setUp(self):
        """Set up test fixtures"""
        self.collector = YahooFinanceDataCollector()
        self.stock = Stock()
        self.stock.m_symbol = "AAPL"

    @patch('data_collector.yahoo_finance_data_collector.yf.Ticker')
    def test_get_stock_info_success(self, mock_ticker):
        """Test successful stock info retrieval"""
        # Mock the yfinance Ticker response
        mock_info = {
            'shortName': 'Apple Inc.',
            'currentPrice': 150.0,
            'bookValue': 3.5,
            'priceToBook': 42.86,
            'dividendYield': 0.005,
            'profitMargins': 0.25,
            'currentRatio': 1.5,
            'debtToEquity': 150.0,
            'marketCap': 2500000000000,
            'returnOnAssets': 0.20,
            'returnOnEquity': 0.30,
            'pegRatio': 2.5,
            'trailingEps': 6.0
        }
        
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.info = mock_info
        mock_ticker.return_value = mock_ticker_instance
        
        self.collector.get_stock_info(self.stock)
        
        self.assertEqual(self.stock.m_company_name, 'Apple Inc.')
        self.assertEqual(self.stock.m_price, 150.0)
        self.assertEqual(self.stock.m_book_value_per_share, 3.5)
        self.assertEqual(self.stock.m_debt_to_equity, 1.5)  # 150/100

    @patch('data_collector.yahoo_finance_data_collector.yf.Ticker')
    def test_get_stock_info_missing_fields(self, mock_ticker):
        """Test handling of missing fields in API response"""
        mock_info = {
            'shortName': 'Test Company'
            # Missing most fields
        }
        
        mock_ticker_instance = MagicMock()
        mock_ticker_instance.info = mock_info
        mock_ticker.return_value = mock_ticker_instance
        
        self.collector.get_stock_info(self.stock)
        
        self.assertEqual(self.stock.m_company_name, 'Test Company')
        self.assertIsNone(self.stock.m_price)
        self.assertEqual(self.stock.m_dividend_yield, 0)

    @patch('data_collector.yahoo_finance_data_collector.yf.Ticker')
    def test_get_stock_info_exception(self, mock_ticker):
        """Test handling of exceptions during data collection"""
        mock_ticker.side_effect = Exception("API Error")
        
        # Should not raise exception, just log it
        self.collector.get_stock_info(self.stock)
        
        # Stock should remain unchanged
        self.assertIsNone(self.stock.m_company_name)


if __name__ == '__main__':
    unittest.main()
