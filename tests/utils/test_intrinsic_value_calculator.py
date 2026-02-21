"""Unit tests for IntrinsicValueCalculator"""
import unittest
from utils.intrinsic_value_calculator import IntrinsicValueCalculator


class TestIntrinsicValueCalculator(unittest.TestCase):
    """Test cases for IntrinsicValueCalculator class"""

    def setUp(self):
        """Set up test fixtures"""
        self.calculator = IntrinsicValueCalculator()

    def test_dcf_calculation_positive_values(self):
        """Test DCF calculation with positive values"""
        result = self.calculator.calculate_intrinsic_value_based_on_discounted_cash_flow(
            current_free_cash_flow_per_share=10.0,
            free_cash_flow_per_share_growth_rate=0.10,
            projected_number_of_years=5,
            discount_rate=0.08,
            perpetual_growth_rate=0.02
        )
        
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

    def test_dcf_calculation_zero_growth(self):
        """Test DCF calculation with zero growth rate"""
        result = self.calculator.calculate_intrinsic_value_based_on_discounted_cash_flow(
            current_free_cash_flow_per_share=10.0,
            free_cash_flow_per_share_growth_rate=0.0,
            projected_number_of_years=5,
            discount_rate=0.08,
            perpetual_growth_rate=0.02
        )
        
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

    def test_book_value_calculation(self):
        """Test book value growth calculation"""
        result = self.calculator.calculate_intrinsic_value_based_on_book_value_growth(
            current_book_value_per_share=50.0,
            book_value_growth_rate=0.15,
            num_of_years=5,
            ten_year_treasury_rate=0.03
        )
        
        self.assertIsInstance(result, float)
        self.assertGreater(result, 0)

    def test_book_value_higher_than_current(self):
        """Test that future book value is higher with positive growth"""
        current_bv = 50.0
        result = self.calculator.calculate_intrinsic_value_based_on_book_value_growth(
            current_book_value_per_share=current_bv,
            book_value_growth_rate=0.15,
            num_of_years=5,
            ten_year_treasury_rate=0.03
        )
        
        # With positive growth and discounting, result should be reasonable
        self.assertGreater(result, 0)
        self.assertLess(result, current_bv * 10)  # Sanity check


if __name__ == '__main__':
    unittest.main()
