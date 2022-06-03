class IntrinsicValueCalculator:
    def calculateIntrinsicValueBasedOnDiscountedCashFlow(
        self,
        currentFreeCashPerShare,
        freeCashPerShareGrowthRate,
        discountRate,  # probably should be WACC
        perpetualGrowthRate,  # Should be conservative, so probably choose inflation rate
    ):
        """
        Args:
        currentFreeCashPerShare: The average free cash per share of the company for the last x years.
        freeCashPerShareGrowthRate: The average free cash per share growth rate of the company for the last x years.
        discountRate:  The rate of return used to determine the present value of future cash flows. Corporations often use the Weighted Average Cost of Capital (WACC).
        perpetualGrowthRate: The constant rate that a company is expected to grow at forever. Usually choose inflation rate.

        Returns:
        The calculated intrinsic value.
        """

        # Calculate discounted cash flow of the next x years.
        discountedCashFlow = 0
        for year in range(1, 10):
            cashFlowAtTheYear = currentFreeCashPerShare * (
                pow((1 + freeCashPerShareGrowthRate), year)
            )
            discountedCashFlow += cashFlowAtTheYear / (pow((1 + discountRate), year))

        # Use Perpetuity Method to calculate the terminal value at x-th year.
        cashFlowOfLastYear = currentFreeCashPerShare * (
            pow((1 + freeCashPerShareGrowthRate), 10)
        )
        terminalValue = (
            cashFlowOfLastYear
            * (1 + perpetualGrowthRate)
            / (discountRate - perpetualGrowthRate)
        )
        discountedTerminalValue = terminalValue / pow(
            (1 + freeCashPerShareGrowthRate), 10
        )

        currentIntrinsicValue = discountedCashFlow + discountedTerminalValue
        return currentIntrinsicValue

    def intrinsicValueBasedOnBookValueGrowth(
        currentBookValuePerShare, bookValueGrowthRate, numOfYears, tenYearTreasuryRate
    ):
        """
        Args:
        currentBookValuePerShare: The current book value per share of the company.
        bookValueGrowthRate: The average book value growth rare of the company for the last x years.
        numOfYears:  Number of years in the future that you want to calculate based on.
        tenYearTreasuryRate: The 10-year treaseury rate.

        Returns:
        The calculated intrinsic value.
        """
        futureBookValue = currentBookValuePerShare * (
            pow((1 + bookValueGrowthRate), numOfYears)
        )
        currentIntrinsicValue = futureBookValue / (
            pow((1 + tenYearTreasuryRate), numOfYears)
        )
        return currentIntrinsicValue


if __name__ == "__main__":
    intrinsicValueCalculator = IntrinsicValueCalculator()
    currentFreeCashPerShare = 3.17
    freeCashPerShareGrowthRate = 0.1390
    discountRate = 0.076
    perpetualGrowthRate = 0.02
    intrinsic_value = (
        intrinsicValueCalculator.calculateIntrinsicValueBasedOnDiscountedCashFlow(
            3.17, 0.1390, 0.076, 0.02
        )
    )
    print(
        """The intrinsic value of a stock with 
                currentFreeCashPerShare = {}, 
                freeCashPerShareGrowthRate = {}, 
                discountRate = {}, 
                perpetualGrowthRate={} is {}""".format(
            3.17,
            0.1390,
            0.076,
            0.02,
            intrinsicValueCalculator.calculateIntrinsicValueBasedOnDiscountedCashFlow(
                3.17, 0.1390, 0.076, 0.02
            ),
        )
    )
    intrinsic_value = (
        intrinsicValueCalculator.calculateIntrinsicValueBasedOnDiscountedCashFlow(
            385.58, 0.1390, 0.076, 0.02
        )
    )
    print(
        """The intrinsic value of a stock with 
                currentFreeCashPerShare = {}, 
                freeCashPerShareGrowthRate = {}, 
                discountRate = {}, 
                perpetualGrowthRate={} is {}""".format(
            385.58,
            0.14,
            0.076,
            0.02,
            intrinsicValueCalculator.calculateIntrinsicValueBasedOnDiscountedCashFlow(
                385.58, 0.14, 0.076, 0.02
            ),
        )
    )
