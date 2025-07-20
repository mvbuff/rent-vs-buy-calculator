# 🏠 Home Ownership vs Rent Calculator

A comprehensive Python application that compares the financial benefits of home ownership versus renting over a specified period of years.

![Python](https://img.shields.io/badge/python-v3.13+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-windows%20%7C%20macOS%20%7C%20linux-lightgrey.svg)

## 🎯 Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/home-ownership-calculator.git
cd home-ownership-calculator

# Run the application
python3 home_calculator.py
```

## 📸 Screenshots

*Add screenshots here to showcase your application*

## Features

- **Scrollable Input Interface**: Organized inputs into logical groups with vertical scrolling (Purchase, Rental, Income & Tax)
- **Detailed Analysis**: Year-by-year breakdown of mortgage payments and rent costs
- **Multiple Views**: Tabbed interface showing mortgage details, rent details, and summary comparison
- **Accurate Calculations**: Uses standard mortgage amortization formulas and compound growth calculations

## Input Categories

### General Settings
- **Number of Years to Compare**: The analysis period (default: 10 years)

### Home Purchase Details
- **Home Price**: Total purchase price of the home
- **Down Payment (%)**: Down payment as percentage of home price
- **30-Year Fixed APR**: Annual percentage rate for the mortgage
- **Property Tax**: Annual property tax rate as percentage of home value (expense only, not tax deductible)
- **House Price Growth**: Expected annual appreciation rate of the home
- **Maintenance Expense Annual**: Annual maintenance and repair costs for the home
- **Brokerage Cost (%)**: Real estate agent commission and fees as percentage of sale price
- **Registration Expenses (%)**: Legal and registration costs as percentage of sale price
- **Capital Gains Tax Benefit**: Checkbox to include tax benefit on home growth (calculated as tax_slab × home_appreciation)

### Rental Details
- **Monthly Rent**: Current monthly rent amount
- **Rent Growth**: Expected annual rent increase percentage

### Income & Tax Details
- **Monthly Income**: Current monthly income
- **Monthly Income Growth**: Expected annual income growth percentage
- **RSUs Income Supplement**: Additional annual income from RSUs/equity
- **IRS Max Tax Slab**: Your marginal tax rate percentage
- **Standard Deduction**: Current IRS standard deduction amount

### Stock Investment Settings
- **Enable Stock Investment Analysis**: Checkbox to enable/disable stock calculations
- **Include Down Payment Growth**: Optional checkbox to include/exclude down payment stock growth
- **Stock Market Growth**: Expected annual return on stock investments (only when enabled)
- **Capital Gains Tax Rate**: Tax rate applied to stock investment gains (default: 20%)

## Output Features

### Mortgage Details Tab
Shows year-by-year breakdown including:
- Monthly EMI amount
- Principal paid each year
- Interest paid each year
- Deductible interest (limited to $750k principal per IRS rules)
- Interest tax savings (tax deduction benefit on mortgage interest)
- Total P&I (Principal & Interest) payments
- Property tax for each year (expense only, no tax deduction)
- Remaining mortgage balance
- Current home value with appreciation

### Rent Details Tab
Shows year-by-year breakdown including:
- Monthly rent amount (with growth)
- Annual rent paid
- EMI-Rent difference (monthly difference between EMI and rent)
- Yearly savings with EMI-Rent difference (annual savings/cost)
- **If stock analysis enabled:**
  - Down payment stock investment value
  - EMI-Rent difference investment accumulation
  - Total stock portfolio value

### Summary Tab
Provides a clear side-by-side comparison in beautified table format:
- **Home Rent vs Home Ownership Cost** comparison table with improved formatting
- **Expenses**: Rent growth vs Interest + Annual maintenance + Buy/sell costs
- **Savings/Income**: EMI-rent difference & stock gains & standard deduction vs Tax deductions & Home growth & Capital gains exemption
- **Net Cost**: Final comparison showing which option costs less
- **Tax deduction strategy**: Standard vs itemized recommendation
- **Net Income Comparison**: Fair comparison showing income minus ALL expenses for both options (home: interest + maintenance + property taxes + selling costs; rental: rent payments + capital gains tax on stock gains)
- **Clear recommendation** with exact savings amount

## How to Run

1. **Prerequisites**: Python 3.13+ (uses only standard library modules)

2. **Launch the application**:
   ```bash
   /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 home_calculator.py
   ```

3. **Using the Application**:
   - Fill in all the input fields with your specific financial data
   - Click "Generate Comparison" to see the analysis
   - Review the three tabs for detailed breakdowns

## Calculation Details

### Mortgage Calculations
- Uses standard amortization formula: `M = P * [r(1+r)^n] / [(1+r)^n - 1]`
- Where M = monthly payment, P = principal, r = monthly interest rate, n = number of payments
- Property tax calculated annually based on current home value
- Home value appreciation compounded annually

### Rent Calculations
- Monthly rent increased annually by the specified growth rate
- Compounded growth: `New Rent = Previous Rent * (1 + growth_rate/100)`

### Summary Analysis
- Compares total cost of ownership vs total rent paid
- Factors in home equity built and final home value
- Shows net financial position for both scenarios

## Example Scenario

Default values represent a typical scenario:
- $1,500,000 home with 20% down payment ($300,000)
- 5.75% APR on 30-year mortgage
- $4,300/month starting rent with 2.5% annual growth
- 3% annual home value growth
- $5,000 annual maintenance expense
- 6% brokerage cost + 2% registration expenses when selling
- 5% expected annual stock market returns
- 5-year comparison period

## Technical Notes

- Built with Python 3.13+ using tkinter for cross-platform compatibility
- No external dependencies required
- Responsive GUI with tabbed results interface
- Error handling for invalid inputs
- Professional styling and formatting

### Key Calculation Details
- **Mortgage Amortization**: Uses standard formula `M = P * [r(1+r)^n] / [(1+r)^n - 1]`
- **Stock Investment Gains**: `down_payment_value_gain + EMI_rent_investments_value_gain` (pure gains only, not total investment)
- **Capital Gains Tax on Stocks**: Applied to stock investment gains as an expense for rental option
- **Tax Deductions**: Mortgage interest only (up to $750k principal) - property tax not deductible
- **Capital Gains**: Tax benefit calculated as tax_slab × home_growth_value (when exemption enabled)
- **Annual Growth**: Applied to house prices, rent, and all other relevant metrics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

If you have any questions or run into issues, please open an issue on GitHub.

## ⭐ Star History

If you find this project helpful, please consider giving it a star! 