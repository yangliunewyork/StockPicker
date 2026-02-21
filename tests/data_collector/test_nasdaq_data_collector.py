"""Unit tests for NasdaqDataCollector"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
from data_collector.nasdaq_data_collector import NasdaqDataCollector


class TestNasdaqDataCollector(unittest.TestCase):
    """Test cases for NasdaqDataCollector class"""

    def setUp(self):
        """Set up test fixtures"""
        self.collector = NasdaqDataCollector()

    @patch('data_collector.nasdaq_data_collector.FTP')
    def test_get_tickers_success(self, mock_ftp_class):
        """Test successful ticker retrieval from NASDAQ FTP"""
        # Mock FTP response
        mock_ftp = MagicMock()
        mock_ftp_class.return_value = mock_ftp
        
        # Simulate FTP file content with proper format
        test_data = "Symbol|Security Name|Market Category|Test Round Lot Size|Financial Status|CQS Symbol|NASDAQ Symbol|NextShares\n"
        test_data += "AAPL|Apple Inc.|Q|100|N|AAPL|AAPL|N\n"
        test_data += "MSFT|Microsoft Corporation|Q|100|N|MSFT|MSFT|N\n"
        test_data += "GOOGL|Alphabet Inc.|Q|100|N|GOOGL|GOOGL|N\n"
        
        # Track what data was written
        written_data = []
        
        def mock_retrbinary(cmd, callback):
            for line in test_data.split('\n'):
                if line:
                    callback(line.encode('utf-8'))
                    callback(b'\n')
        
        mock_ftp.retrbinary = mock_retrbinary
        
        tickers = self.collector.get_tickers()
        
        self.assertIsInstance(tickers, list)
        self.assertGreater(len(tickers), 0)
        # Check that we got some tickers (the exact list depends on parsing)
        self.assertIn('AAPL', tickers)
        mock_ftp.login.assert_called_once()
        mock_ftp.quit.assert_called_once()

    @patch('data_collector.nasdaq_data_collector.FTP')
    def test_get_tickers_ftp_error(self, mock_ftp_class):
        """Test handling of FTP connection errors"""
        mock_ftp_class.side_effect = Exception("FTP Connection Failed")
        
        tickers = self.collector.get_tickers()
        
        self.assertIsInstance(tickers, list)
        self.assertEqual(len(tickers), 0)


if __name__ == '__main__':
    unittest.main()
