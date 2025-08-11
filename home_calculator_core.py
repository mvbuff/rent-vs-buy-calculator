#!/usr/bin/env python3
"""
Home Calculator Core Module
Contains all financial calculations shared between desktop and web versions
"""

import math
from typing import Dict, List, Tuple, Any


class HomeCalculatorCore:
    """Core calculation engine for home ownership vs rent analysis"""
    
    @staticmethod
    def calculate_mortgage_payment(principal: float, annual_rate: float, years: int = 30) -> float:
        """
        Calculate monthly mortgage payment using standard amortization formula
        
        Args:
            principal: Loan principal amount
            annual_rate: Annual interest rate (percentage)
            years: Loan term in years (default 30)
            
        Returns:
            Monthly payment amount
        """
        monthly_rate = annual_rate / 100 / 12
        num_payments = years * 12
        
        if monthly_rate == 0:
            return principal / num_payments
        
        payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
                 ((1 + monthly_rate)**num_payments - 1)
        return payment
    
    @staticmethod
    def generate_mortgage_data(
        home_price: float,
        down_payment_pct: float,
        apr: float,
        property_tax_rate: float,
        property_tax_growth: float,
        house_growth: float,
        tax_rate: float,
        years: int
    ) -> List[Dict[str, Any]]:
        """
        Generate year-by-year mortgage amortization data
        
        Args:
            home_price: Initial home price
            down_payment_pct: Down payment percentage
            apr: Annual percentage rate
            property_tax_rate: Property tax rate (percentage)
            property_tax_growth: Annual property tax growth rate (percentage, CA Prop 13 = 2%)
            house_growth: Annual home price growth rate (percentage)
            tax_rate: Income tax rate for deduction calculations (percentage)
            years: Number of years to analyze
            
        Returns:
            List of dictionaries containing yearly mortgage data
        """
        down_payment = home_price * (down_payment_pct / 100)
        loan_amount = home_price - down_payment
        monthly_payment = HomeCalculatorCore.calculate_mortgage_payment(loan_amount, apr, 30)
        
        mortgage_data = []
        current_balance = loan_amount
        current_home_value = home_price
        current_property_tax_base = home_price  # Separate tax base for Prop 13
        
        for year in range(1, years + 1):
            # Mortgage calculations
            annual_payment = monthly_payment * 12
            year_interest = current_balance * (apr / 100)
            year_principal = annual_payment - year_interest
            current_balance = max(0, current_balance - year_principal)
            current_home_value *= (1 + house_growth / 100)
            
            # Property tax calculation with Prop 13 limits
            current_property_tax_base *= (1 + property_tax_growth / 100)
            annual_property_tax = current_property_tax_base * (property_tax_rate / 100)
            
            # Interest tax deduction (limited to $750k principal)
            deductible_principal_limit = 750000
            current_loan_balance = min(current_balance + year_principal, deductible_principal_limit)
            deductible_interest = year_interest * (current_loan_balance / (current_balance + year_principal)) if (current_balance + year_principal) > 0 else year_interest
            interest_tax_savings = deductible_interest * (tax_rate / 100)
            
            mortgage_data.append({
                'Year': year,
                'Monthly EMI': monthly_payment,
                'Principal Paid': year_principal,
                'Interest Paid': year_interest,
                'Deductible Interest': deductible_interest,
                'Interest Tax Savings': interest_tax_savings,
                'Total P&I': year_principal + year_interest,
                'Property Tax': annual_property_tax,
                'Remaining Balance': current_balance,
                'Home Value': current_home_value
            })
        
        return mortgage_data
    
    @staticmethod
    def generate_rent_data(
        monthly_rent: float,
        rent_growth: float,
        monthly_payment: float,
        down_payment: float,
        stock_growth: float,
        years: int,
        stocks_enabled: bool = True,
        include_down_payment_growth: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Generate year-by-year rental and investment data
        
        Args:
            monthly_rent: Initial monthly rent
            rent_growth: Annual rent growth rate (percentage)
            monthly_payment: Monthly mortgage payment for EMI-rent difference
            down_payment: Down payment amount for investment
            stock_growth: Annual stock market growth rate (percentage)
            years: Number of years to analyze
            stocks_enabled: Whether to calculate stock investments
            include_down_payment_growth: Whether down payment grows with stocks
            
        Returns:
            List of dictionaries containing yearly rent and investment data
        """
        rent_data = []
        current_rent = monthly_rent
        cumulative_emi_rent_diff_investment = 0
        
        for year in range(1, years + 1):
            annual_rent = current_rent * 12
            monthly_emi_rent_diff = monthly_payment - current_rent
            annual_emi_rent_diff = monthly_emi_rent_diff * 12
            monthly_emi_rent_diff_positive = max(0, monthly_emi_rent_diff)
            annual_emi_rent_diff_positive = monthly_emi_rent_diff_positive * 12
            
            year_data = {
                'Year': year,
                'Monthly Rent': current_rent,
                'Annual Rent': annual_rent,
                'EMI-Rent Diff': monthly_emi_rent_diff,
                'Yearly Savings with EMI-Rent Diff': annual_emi_rent_diff
            }
            
            if stocks_enabled:
                # Calculate stock growth on down payment (only if enabled)
                if include_down_payment_growth:
                    down_payment_value = down_payment * ((1 + stock_growth/100) ** year)
                else:
                    down_payment_value = down_payment
                
                # Calculate stock growth on accumulated EMI-rent difference investments
                if year == 1:
                    cumulative_emi_rent_diff_investment = annual_emi_rent_diff_positive
                else:
                    cumulative_emi_rent_diff_investment = (cumulative_emi_rent_diff_investment * (1 + stock_growth/100)) + annual_emi_rent_diff_positive
                
                total_stock_investment_value = down_payment_value + cumulative_emi_rent_diff_investment
                
                year_data.update({
                    'Down Payment Investment': down_payment_value,
                    'EMI-Rent Diff Investment': cumulative_emi_rent_diff_investment,
                    'Total Stock Value': total_stock_investment_value
                })
            
            rent_data.append(year_data)
            current_rent *= (1 + rent_growth / 100)
        
        return rent_data
    
    @staticmethod
    def calculate_summary_metrics(
        mortgage_data: List[Dict],
        rent_data: List[Dict],
        inputs: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive summary metrics for comparison
        
        Args:
            mortgage_data: Year-by-year mortgage data
            rent_data: Year-by-year rent data
            inputs: Dictionary containing all input parameters
            
        Returns:
            Dictionary containing all summary metrics
        """
        # Extract totals from data
        total_rent = sum([row['Annual Rent'] for row in rent_data])
        total_interest = sum([row['Interest Paid'] for row in mortgage_data])
        total_property_tax = sum([row['Property Tax'] for row in mortgage_data])
        total_interest_tax_savings = sum([row['Interest Tax Savings'] for row in mortgage_data])
        
        # Calculate final values
        final_home_value = mortgage_data[-1]['Home Value']
        initial_home_value = inputs['home_price']
        home_sale_gains = final_home_value - initial_home_value
        
        # Calculate selling costs
        total_selling_costs = final_home_value * ((inputs['brokerage_cost'] + inputs['registration_cost']) / 100)
        
        # Calculate capital gains tax benefit using long-term capital gains rate
        home_capital_gains_rate = inputs.get('capital_gains_tax_rate', 20.0) if inputs.get('capital_gains_tax_rate', 0) > 0 else 20.0
        if inputs.get('capital_gains_exemption_enabled', True) and home_sale_gains > 0:
            capital_gains_tax_savings = home_sale_gains * (home_capital_gains_rate / 100)
        else:
            capital_gains_tax_savings = 0
        
        # Calculate stock investment gains if enabled
        stock_investment_gains = 0
        capital_gains_tax_owed = 0
        
        if inputs.get('stocks_enabled', False):
            final_down_payment_value = rent_data[-1].get('Down Payment Investment', 0)
            final_emi_rent_diff_investment = rent_data[-1].get('EMI-Rent Diff Investment', 0)
            
            if inputs.get('include_down_payment_growth', True):
                down_payment_value_gain = final_down_payment_value - inputs['home_price'] * (inputs['down_payment_pct'] / 100)
            else:
                down_payment_value_gain = 0
            
            # Calculate total EMI-rent difference invested
            monthly_payment = HomeCalculatorCore.calculate_mortgage_payment(
                inputs['home_price'] * (1 - inputs['down_payment_pct']/100), 
                inputs['apr'], 
                30
            )
            total_emi_rent_diff_invested = sum([
                max(0, (monthly_payment * 12) - row['Annual Rent'])
                for row in rent_data
            ])
            
            emi_rent_investments_value_gain = final_emi_rent_diff_investment - total_emi_rent_diff_invested
            stock_investment_gains = down_payment_value_gain + emi_rent_investments_value_gain
            capital_gains_tax_owed = stock_investment_gains * (inputs.get('capital_gains_tax_rate', 20.0) / 100)
        
        # Calculate net costs
        total_maintenance = inputs.get('maintenance_annual', 0) * inputs['years']
        rental_standard_deduction_benefit = inputs.get('standard_deduction', 0) * inputs['years'] * (inputs['tax_rate'] / 100)
        
        rent_net_cost = total_rent + capital_gains_tax_owed - stock_investment_gains - rental_standard_deduction_benefit
        ownership_net_cost = total_interest + total_maintenance + total_property_tax + total_selling_costs - (total_interest_tax_savings + capital_gains_tax_savings) - home_sale_gains
        
        return {
            'total_rent': total_rent,
            'total_interest': total_interest,
            'total_property_tax': total_property_tax,
            'total_maintenance': total_maintenance,
            'total_selling_costs': total_selling_costs,
            'home_sale_gains': home_sale_gains,
            'total_interest_tax_savings': total_interest_tax_savings,
            'capital_gains_tax_savings': capital_gains_tax_savings,
            'home_capital_gains_rate': home_capital_gains_rate,
            'stock_investment_gains': stock_investment_gains,
            'capital_gains_tax_owed': capital_gains_tax_owed,
            'rental_standard_deduction_benefit': rental_standard_deduction_benefit,
            'rent_net_cost': rent_net_cost,
            'ownership_net_cost': ownership_net_cost,
            'winner': 'HOME OWNERSHIP' if ownership_net_cost < rent_net_cost else 'RENTING',
            'savings': abs(ownership_net_cost - rent_net_cost)
        }
    
    @staticmethod
    def generate_complete_analysis(inputs: Dict[str, Any]) -> Tuple[List[Dict], List[Dict], Dict[str, Any]]:
        """
        Generate complete financial analysis for home ownership vs rent
        
        Args:
            inputs: Dictionary containing all input parameters
            
        Returns:
            Tuple of (mortgage_data, rent_data, summary_metrics)
        """
        # Generate mortgage data
        mortgage_data = HomeCalculatorCore.generate_mortgage_data(
            home_price=inputs['home_price'],
            down_payment_pct=inputs['down_payment_pct'],
            apr=inputs['apr'],
            property_tax_rate=inputs['property_tax_rate'],
            property_tax_growth=inputs.get('property_tax_growth', 2.0),  # Default CA Prop 13 limit
            house_growth=inputs['house_growth'],
            tax_rate=inputs['tax_rate'],
            years=inputs['years']
        )
        
        # Calculate mortgage payment and down payment for rent analysis
        down_payment = inputs['home_price'] * (inputs['down_payment_pct'] / 100)
        loan_amount = inputs['home_price'] - down_payment
        monthly_payment = HomeCalculatorCore.calculate_mortgage_payment(loan_amount, inputs['apr'], 30)
        
        # Generate rent data
        rent_data = HomeCalculatorCore.generate_rent_data(
            monthly_rent=inputs['monthly_rent'],
            rent_growth=inputs['rent_growth'],
            monthly_payment=monthly_payment,
            down_payment=down_payment,
            stock_growth=inputs.get('stock_growth', 8.0),
            years=inputs['years'],
            stocks_enabled=inputs.get('stocks_enabled', False),
            include_down_payment_growth=inputs.get('include_down_payment_growth', True)
        )
        
        # Calculate summary metrics
        summary = HomeCalculatorCore.calculate_summary_metrics(mortgage_data, rent_data, inputs)
        
        return mortgage_data, rent_data, summary


# Default input values for consistency across versions
DEFAULT_VALUES = {
    'years': 5,
    'home_price': 1500000,
    'down_payment_pct': 20.0,
    'apr': 5.75,
    'property_tax_rate': 1.25,
    'property_tax_growth': 2.0,  # CA Proposition 13 limit
    'house_growth': 3.0,
    'maintenance_annual': 10000,
    'brokerage_cost': 6.0,
    'registration_cost': 2.0,
    'monthly_rent': 4500,
    'rent_growth': 5.0,
    'monthly_income': 8000,
    'income_growth': 4.0,
    'rsu_income': 0,
    'tax_rate': 35.0,
    'standard_deduction': 0,
    'stocks_enabled': True,
    'include_down_payment_growth': True,
    'stock_growth': 8.0,
    'capital_gains_tax_rate': 20.0,
    'capital_gains_exemption_enabled': True
}
