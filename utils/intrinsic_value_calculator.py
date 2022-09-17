"""
A module for intrinsic value calculation.
"""


class IntrinsicValueCalculator:
    """
    A utility class that provides different ways of calculating intrinsic value.
    """

    def calculate_intrinsic_value_based_on_discounted_cash_flow(
        self,
        current_free_cash_flow_per_share,
        free_cash_flow_per_share_growth_rate,
        projected_number_of_years,
        discount_rate,
        perpetual_growth_rate,
    ):
        """
        Args:
            current_free_cash_flow_per_share: Current free cash flow per share.
            free_cash_per_share_growth_rate: The average free cash per share growth rate
                of the company for the last x years.
            projected_number_of_years: Typically, a target’s FCF is projected out 5 to 10 years in the future.
            discount_rate:  The rate of return used to determine the
                present value of future cash flows. Corporations often use the
                Weighted Average Cost of Capital (WACC).
            perpetual_growth_rate: The constant rate that a company is expected to
                grow at forever. Usually choose inflation rate.

        Returns:
            The calculated intrinsic value.
        """

        # Calculate discounted cash flow of the next x years.
        discounted_cash_flow = 0
        for year in range(1, projected_number_of_years):
            cash_flow_at_the_year = current_free_cash_flow_per_share * (
                pow((1 + free_cash_flow_per_share_growth_rate), year)
            )
            discounted_cash_flow += cash_flow_at_the_year / (
                pow((1 + discount_rate), year)
            )

        # Use Perpetuity Method to calculate the terminal value at x-th year.
        cash_flow_of_last_year = current_free_cash_flow_per_share * (
            pow((1 + free_cash_flow_per_share_growth_rate), projected_number_of_years)
        )
        terminal_value = (
            cash_flow_of_last_year
            * (1 + perpetual_growth_rate)
            / (discount_rate - perpetual_growth_rate)
        )
        discounted_terminal_value = terminal_value / pow(
            (1 + free_cash_flow_per_share_growth_rate), projected_number_of_years
        )

        current_intrinsic_value = discounted_cash_flow + discounted_terminal_value
        return current_intrinsic_value

    def calculate_intrinsic_value_based_on_book_value_growth(
        self,
        current_book_value_per_share,
        book_value_growth_rate,
        num_of_years,
        ten_year_treasury_rate,
    ):
        """
        Args:
        current_book_value_per_share:
            The current book value per share of the company.
        book_value_growth_rate:
            The average book value growth rare of the company for the last x years.
        num_of_years:
            Number of years in the future that you want to calculate based on.
        ten_year_treasury_rate:
            The 10-year treaseury rate.

        Returns:
            The calculated intrinsic value.
        """
        future_book_value = current_book_value_per_share * (
            pow((1 + book_value_growth_rate), num_of_years)
        )
        current_intrinsic_value = future_book_value / (
            pow((1 + ten_year_treasury_rate), num_of_years)
        )
        return current_intrinsic_value


if __name__ == "__main__":
    intrinsic_value_calculator = IntrinsicValueCalculator()
    intrinsic_value = intrinsic_value_calculator.calculate_intrinsic_value_based_on_discounted_cash_flow(
        3.17, 0.1390, 0.076, 0.02
    )
    print(
        f"""The intrinsic value of a stock with
                current_free_cash_per_share = {3.17},
                free_cash_per_share_growth_rate = {0.1390},
                discount_rate = {0.076},
                perpetual_growth_rate={0.02} is {
                    intrinsic_value_calculator.calculate_intrinsic_value_based_on_discounted_cash_flow(
                    3.17, 0.1390, 0.076, 0.02
                    )
                }
        """
    )

    print(
        f"""
            The intrinsic value of a stock with
                current_free_cash_per_share = {385.58},
                free_cash_per_share_growth_rate = {0.14},
                discount_rate = {0.076},
                perpetual_growth_rate={0.02} is {
                    intrinsic_value_calculator
                    .calculate_intrinsic_value_based_on_discounted_cash_flow(
                        385.58, 0.14, 0.076, 0.02)
                }
        """
    )
