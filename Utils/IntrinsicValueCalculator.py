class IntrinsicValueCalculator:
    def intrinsicValueBasedOnDiscountedCashFlow(
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