class IntrinsicValueCalculator:
    def calculateIntrinsicValueBasedOnDiscountedCashFlow(
        self,
        currentFreeCashPerShare, 
        freeCashPerShareGrowthRate,
        discountedRate, # probably should be WACC
        perpetualGrowthRate # Should be conservative, so probably choose inflation rate
        ): 
        discountedCashFlow = 0
        for year in range(1, 10):
            cashFlowAtTheYear = currentFreeCashPerShare * (pow((1 + freeCashPerShareGrowthRate), year))
            discountedCashFlow += cashFlowAtTheYear /  (pow((1 + discountedRate), year))
            
        # Use Perpetuity Method to calculate the terminal value    
        cashFlowOfLastYear =  currentFreeCashPerShare * (pow((1 + freeCashPerShareGrowthRate), 10))
        terminalValue = cashFlowOfLastYear * (1 + perpetualGrowthRate) / (discountedRate - perpetualGrowthRate)
        discountedTerminalValue = terminalValue/ pow((1 + freeCashPerShareGrowthRate), 10)
        
        currentIntrinsicValue = discountedCashFlow + discountedTerminalValue
        return currentIntrinsicValue


if __name__ == "__main__":
    intrinsicValueCalculator = IntrinsicValueCalculator()
    currentFreeCashPerShare = 3.17
    freeCashPerShareGrowthRate = 0.1390
    discountedRate = 0.076
    perpetualGrowthRate = 0.02
    intrinsic_value = intrinsicValueCalculator.calculateIntrinsicValueBasedOnDiscountedCashFlow(3.17, 0.1390, 0.076, 0.02)
    print ("""The intrinsic value of a stock with 
                currentFreeCashPerShare = {}, 
                freeCashPerShareGrowthRate = {}, 
                discountedRate = {}, 
                perpetualGrowthRate={} is {}"""
                .format(3.17, 0.1390, 0.076, 0.02, 
                    intrinsicValueCalculator.calculateIntrinsicValueBasedOnDiscountedCashFlow(3.17, 0.1390, 0.076, 0.02)
                )
    )
    intrinsic_value = intrinsicValueCalculator.calculateIntrinsicValueBasedOnDiscountedCashFlow(385.58, 0.1390, 0.076, 0.02)
    print ("""The intrinsic value of a stock with 
                currentFreeCashPerShare = {}, 
                freeCashPerShareGrowthRate = {}, 
                discountedRate = {}, 
                perpetualGrowthRate={} is {}""".format(385.58, 0.14, 0.076, 0.02, 
                    intrinsicValueCalculator.calculateIntrinsicValueBasedOnDiscountedCashFlow(385.58, 0.14, 0.076, 0.02)
                )
    )