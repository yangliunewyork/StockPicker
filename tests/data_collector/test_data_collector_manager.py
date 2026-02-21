"""Unit tests for DataCollectorManager"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from data_collector.data_collector_manager import DataCollectorManager
from model.stock import Stock


class TestDataCollectorManager(unittest.TestCase):
    """Test cases for DataCollectorManager class"""

    def setUp(self):
        """Set up test fixtures"""
        self.manager = DataCollectorManager()

    @patch('data_collector.data_collector_manager.NasdaqDataCollector')
    def test_get_stock_tickers(self, mock_nasdaq_class):
        """Test getting stock tickers from NASDAQ"""
        mock_nasdaq = MagicMock()
        mock_nasdaq.get_tickers.return_value = ['AAPL', 'MSFT', 'GOOGL']
        mock_nasdaq_class.return_value = mock_nasdaq
        
        tickers = self.manager.get_stock_tickers()
        
        self.assertIsInstance(tickers, list)
        self.assertEqual(len(tickers), 3)
        self.assertIn('AAPL', tickers)

    @patch('data_collector.data_collector_manager.YahooFinanceDataCollector')
    def test_gather_stock_information(self, mock_yahoo_class):
        """Test gathering stock information"""
        mock_yahoo = MagicMock()
        mock_yahoo_class.return_value = mock_yahoo
        
        # Create test stocks
        stocks = [Stock(), Stock()]
        stocks[0].m_symbol = "AAPL"
        stocks[1].m_symbol = "MSFT"
        
        # Recreate manager to use mocked collector
        manager = DataCollectorManager()
        manager._yahoo_finance_data_collector = mock_yahoo
        
        manager.gather_stock_information(stocks)
        
        # Verify Yahoo Finance collector was called for each stock
        self.assertEqual(mock_yahoo.get_stock_info.call_count, 2)


if __name__ == '__main__':
    unittest.main()
