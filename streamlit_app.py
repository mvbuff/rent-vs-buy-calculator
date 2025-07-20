#!/usr/bin/env python3

import streamlit as st
import pandas as pd
import math

# Page configuration
st.set_page_config(
    page_title="🏠 Home Ownership vs Rent Calculator",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        color: #2c3e50;
    }
    .metric-card {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .comparison-table {
        border: 2px solid #3498db;
        border-radius: 10px;
        padding: 20px;
        margin: 20px 0;
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

class HomeCalculator:
    def __init__(self):
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'calculated' not in st.session_state:
            st.session_state.calculated = False
    
    def calculate_mortgage_payment(self, principal, annual_rate, years):
        """Calculate monthly mortgage payment using standard formula"""
        monthly_rate = annual_rate / 100 / 12
        num_payments = years * 12
        
        if monthly_rate == 0:
            return principal / num_payments
        
        payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
                 ((1 + monthly_rate)**num_payments - 1)
        return payment
    
    def generate_analysis(self, inputs):
        """Generate the complete financial analysis"""
        # Extract inputs
        years = inputs['years']
        home_price = inputs['home_price']
        down_payment_pct = inputs['down_payment_pct']
        apr = inputs['apr']
        property_tax_rate = inputs['property_tax_rate']
        house_growth = inputs['house_growth']
        maintenance_annual = inputs['maintenance_annual']
        brokerage_cost = inputs['brokerage_cost']
        registration_cost = inputs['registration_cost']
        monthly_rent = inputs['monthly_rent']
        rent_growth = inputs['rent_growth']
        monthly_income = inputs['monthly_income']
        income_growth = inputs['income_growth']
        rsu_income = inputs['rsu_income']
        tax_rate = inputs['tax_rate']
        standard_deduction = inputs['standard_deduction']
        stocks_enabled = inputs['stocks_enabled']
        include_down_payment_growth = inputs['include_down_payment_growth']
        stock_growth = inputs['stock_growth']
        capital_gains_tax_rate = inputs['capital_gains_tax_rate']
        capital_gains_exemption_enabled = inputs['capital_gains_exemption_enabled']
        
        # Calculate derived values
        down_payment = home_price * (down_payment_pct / 100)
        loan_amount = home_price - down_payment
        monthly_payment = self.calculate_mortgage_payment(loan_amount, apr, 30)
        monthly_property_tax = home_price * (property_tax_rate / 100) / 12
        
        # Generate year-by-year data
        mortgage_data = []
        rent_data = []
        
        current_balance = loan_amount
        current_home_value = home_price
        current_rent = monthly_rent
        cumulative_emi_rent_diff_investment = 0
        
        for year in range(1, years + 1):
            # Mortgage calculations
            annual_payment = monthly_payment * 12
            year_interest = current_balance * (apr / 100)
            year_principal = annual_payment - year_interest
            current_balance = max(0, current_balance - year_principal)
            current_home_value *= (1 + house_growth / 100)
            annual_property_tax = current_home_value * (property_tax_rate / 100)
            
            # Interest tax deduction (limited to $750k principal)
            deductible_principal_limit = 750000
            current_loan_balance = min(current_balance + year_principal, deductible_principal_limit)
            deductible_interest = year_interest * (current_loan_balance / (current_balance + year_principal)) if (current_balance + year_principal) > 0 else year_interest
            interest_tax_savings = deductible_interest * (tax_rate / 100)
            
            mortgage_data.append({
                'Year': year,
                'Monthly EMI': f"${monthly_payment:,.2f}",
                'Principal Paid': f"${year_principal:,.2f}",
                'Interest Paid': f"${year_interest:,.2f}",
                'Deductible Interest': f"${deductible_interest:,.2f}",
                'Interest Tax Savings': f"${interest_tax_savings:,.2f}",
                'Total P&I': f"${year_principal + year_interest:,.2f}",
                'Property Tax': f"${annual_property_tax:,.2f}",
                'Remaining Balance': f"${current_balance:,.2f}",
                'Home Value': f"${current_home_value:,.2f}"
            })
            
            # Rent calculations
            annual_rent = current_rent * 12
            monthly_emi_rent_diff = monthly_payment - current_rent
            annual_emi_rent_diff = monthly_emi_rent_diff * 12
            monthly_emi_rent_diff_positive = max(0, monthly_emi_rent_diff)
            annual_emi_rent_diff_positive = monthly_emi_rent_diff_positive * 12
            
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
                
                rent_data.append({
                    'Year': year,
                    'Monthly Rent': f"${current_rent:,.2f}",
                    'Annual Rent': f"${annual_rent:,.2f}",
                    'EMI-Rent Diff': f"${monthly_emi_rent_diff:,.2f}",
                    'Yearly Savings with EMI-Rent Diff': f"${annual_emi_rent_diff:,.2f}",
                    'Down Payment Investment': f"${down_payment_value:,.2f}",
                    'EMI-Rent Diff Investment': f"${cumulative_emi_rent_diff_investment:,.2f}",
                    'Total Stock Value': f"${total_stock_investment_value:,.2f}"
                })
            else:
                rent_data.append({
                    'Year': year,
                    'Monthly Rent': f"${current_rent:,.2f}",
                    'Annual Rent': f"${annual_rent:,.2f}",
                    'EMI-Rent Diff': f"${monthly_emi_rent_diff:,.2f}",
                    'Yearly Savings with EMI-Rent Diff': f"${annual_emi_rent_diff:,.2f}"
                })
            
            current_rent *= (1 + rent_growth / 100)
        
        return mortgage_data, rent_data, self.calculate_summary(mortgage_data, rent_data, inputs)
    
    def calculate_summary(self, mortgage_data, rent_data, inputs):
        """Calculate summary statistics"""
        # Extract necessary values from data
        total_rent = sum([float(row['Annual Rent'].replace('$', '').replace(',', '')) for row in rent_data])
        total_interest = sum([float(row['Interest Paid'].replace('$', '').replace(',', '')) for row in mortgage_data])
        total_property_tax = sum([float(row['Property Tax'].replace('$', '').replace(',', '')) for row in mortgage_data])
        total_interest_tax_savings = sum([float(row['Interest Tax Savings'].replace('$', '').replace(',', '')) for row in mortgage_data])
        
        # Calculate final values
        final_home_value = float(mortgage_data[-1]['Home Value'].replace('$', '').replace(',', ''))
        initial_home_value = inputs['home_price']
        home_sale_gains = final_home_value - initial_home_value
        
        # Calculate selling costs
        total_selling_costs = final_home_value * ((inputs['brokerage_cost'] + inputs['registration_cost']) / 100)
        
        # Calculate capital gains tax benefit
        if inputs['capital_gains_exemption_enabled'] and home_sale_gains > 0:
            capital_gains_tax_savings = home_sale_gains * (inputs['tax_rate'] / 100)
        else:
            capital_gains_tax_savings = 0
        
        # Calculate stock investment gains if enabled
        if inputs['stocks_enabled']:
            final_down_payment_value = float(rent_data[-1]['Down Payment Investment'].replace('$', '').replace(',', ''))
            final_emi_rent_diff_investment = float(rent_data[-1]['EMI-Rent Diff Investment'].replace('$', '').replace(',', ''))
            
            if inputs['include_down_payment_growth']:
                down_payment_value_gain = final_down_payment_value - inputs['home_price'] * (inputs['down_payment_pct'] / 100)
            else:
                down_payment_value_gain = 0
            
            total_emi_rent_diff_invested = sum([
                max(0, (float(mortgage_data[0]['Monthly EMI'].replace('$', '').replace(',', '')) * 12) - float(row['Annual Rent'].replace('$', '').replace(',', '')))
                for row in rent_data
            ])
            emi_rent_investments_value_gain = final_emi_rent_diff_investment - total_emi_rent_diff_invested
            stock_investment_gains = down_payment_value_gain + emi_rent_investments_value_gain
            capital_gains_tax_owed = stock_investment_gains * (inputs['capital_gains_tax_rate'] / 100)
        else:
            stock_investment_gains = 0
            capital_gains_tax_owed = 0
        
        # Calculate net costs
        total_maintenance = inputs['maintenance_annual'] * inputs['years']
        rental_standard_deduction_benefit = inputs['standard_deduction'] * inputs['years'] * (inputs['tax_rate'] / 100)
        
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
            'stock_investment_gains': stock_investment_gains,
            'capital_gains_tax_owed': capital_gains_tax_owed,
            'rental_standard_deduction_benefit': rental_standard_deduction_benefit,
            'rent_net_cost': rent_net_cost,
            'ownership_net_cost': ownership_net_cost,
            'winner': 'HOME OWNERSHIP' if ownership_net_cost < rent_net_cost else 'RENTING',
            'savings': abs(ownership_net_cost - rent_net_cost)
        }

def main():
    # Header
    st.markdown("<h1 class='main-header'>🏠 Home Ownership vs Rent Calculator</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    calculator = HomeCalculator()
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("📊 Input Parameters")
        
        # General Settings
        st.subheader("⏱️ General Settings")
        years = st.number_input("Number of Years to Compare", min_value=1, max_value=50, value=5)
        
        # Home Purchase Details
        st.subheader("🏠 Home Purchase Details")
        home_price = st.number_input("Home Price ($)", min_value=50000, max_value=10000000, value=1500000, step=10000)
        down_payment_pct = st.number_input("Down Payment (%)", min_value=0.0, max_value=100.0, value=20.0, step=0.5)
        apr = st.number_input("30-Year Fixed APR (%)", min_value=0.1, max_value=20.0, value=5.75, step=0.01)
        property_tax_rate = st.number_input("Property Tax (% per year)", min_value=0.0, max_value=10.0, value=1.2, step=0.01)
        house_growth = st.number_input("House Price Growth (% per year)", min_value=-10.0, max_value=50.0, value=3.0, step=0.1)
        maintenance_annual = st.number_input("Maintenance Expense Annual ($)", min_value=0, max_value=100000, value=10000, step=500)
        brokerage_cost = st.number_input("Brokerage Cost (% of sale price)", min_value=0.0, max_value=20.0, value=6.0, step=0.1)
        registration_cost = st.number_input("Registration Expenses (% of sale price)", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
        capital_gains_exemption_enabled = st.checkbox("Include Capital Gains Tax Benefit on Home Growth", value=True)
        
        # Rental Details
        st.subheader("🏠 Rental Details")
        monthly_rent = st.number_input("Monthly Rent ($)", min_value=500, max_value=50000, value=4300, step=50)
        rent_growth = st.number_input("Rent Growth (% per year)", min_value=0.0, max_value=20.0, value=3.0, step=0.1)
        
        # Income & Tax Details
        st.subheader("💰 Income & Tax Details")
        monthly_income = st.number_input("Monthly Income ($)", min_value=1000, max_value=200000, value=8000, step=500)
        income_growth = st.number_input("Monthly Income Growth (% per year)", min_value=0.0, max_value=50.0, value=4.0, step=0.1)
        rsu_income = st.number_input("RSUs Income Supplement ($)", min_value=0, max_value=1000000, value=0, step=1000)
        tax_rate = st.number_input("IRS Max Tax Slab (%)", min_value=0.0, max_value=50.0, value=35.0, step=0.5)
        standard_deduction = st.number_input("Standard Deduction ($)", min_value=0, max_value=100000, value=0, step=1000)
        
        # Stock Investment Settings
        st.subheader("📈 Stock Investment Settings")
        stocks_enabled = st.checkbox("Enable Stock Investment Analysis", value=True)
        if stocks_enabled:
            include_down_payment_growth = st.checkbox("Include Down Payment Growth", value=True)
            stock_growth = st.number_input("Stock Market Growth (% per year)", min_value=0.0, max_value=50.0, value=8.0, step=0.1)
            capital_gains_tax_rate = st.number_input("Capital Gains Tax Rate (%)", min_value=0.0, max_value=50.0, value=20.0, step=0.5)
        else:
            include_down_payment_growth = False
            stock_growth = 0
            capital_gains_tax_rate = 0
    
    # Collect all inputs
    inputs = {
        'years': years, 'home_price': home_price, 'down_payment_pct': down_payment_pct,
        'apr': apr, 'property_tax_rate': property_tax_rate, 'house_growth': house_growth,
        'maintenance_annual': maintenance_annual, 'brokerage_cost': brokerage_cost,
        'registration_cost': registration_cost, 'capital_gains_exemption_enabled': capital_gains_exemption_enabled,
        'monthly_rent': monthly_rent, 'rent_growth': rent_growth, 'monthly_income': monthly_income,
        'income_growth': income_growth, 'rsu_income': rsu_income, 'tax_rate': tax_rate,
        'standard_deduction': standard_deduction, 'stocks_enabled': stocks_enabled,
        'include_down_payment_growth': include_down_payment_growth, 'stock_growth': stock_growth,
        'capital_gains_tax_rate': capital_gains_tax_rate
    }
    
    # Generate Analysis Button
    if st.button("🚀 Generate Comparison", type="primary", use_container_width=True):
        with st.spinner("Calculating financial analysis..."):
            mortgage_data, rent_data, summary = calculator.generate_analysis(inputs)
            st.session_state.mortgage_data = mortgage_data
            st.session_state.rent_data = rent_data
            st.session_state.summary = summary
            st.session_state.calculated = True
            st.rerun()
    
    # Display results if calculated
    if st.session_state.calculated and hasattr(st.session_state, 'summary'):
        st.markdown("---")
        
        # Summary Cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class='metric-card'>
                <h3>🏠 Home Ownership</h3>
                <h2>${st.session_state.summary['ownership_net_cost']:,.0f}</h2>
                <p>Total Net Cost</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='metric-card'>
                <h3>🏠 Rental</h3>
                <h2>${st.session_state.summary['rent_net_cost']:,.0f}</h2>
                <p>Total Net Cost</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            winner_color = "#27ae60" if st.session_state.summary['winner'] == 'HOME OWNERSHIP' else "#e74c3c"
            st.markdown(f"""
            <div class='metric-card' style='background: {winner_color}'>
                <h3>🏆 Winner</h3>
                <h2>{st.session_state.summary['winner']}</h2>
                <p>Saves ${st.session_state.summary['savings']:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Detailed Analysis Tabs
        tab1, tab2, tab3 = st.tabs(["📊 Mortgage Details", "🏠 Rent Details", "📋 Summary"])
        
        with tab1:
            st.subheader("📊 Mortgage Details")
            df_mortgage = pd.DataFrame(st.session_state.mortgage_data)
            st.dataframe(df_mortgage, use_container_width=True)
        
        with tab2:
            st.subheader("🏠 Rent Details")
            df_rent = pd.DataFrame(st.session_state.rent_data)
            st.dataframe(df_rent, use_container_width=True)
        
        with tab3:
            st.subheader("📋 Financial Summary")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🏠 Home Ownership Costs")
                st.write(f"**Total Interest Paid:** ${st.session_state.summary['total_interest']:,.0f}")
                st.write(f"**Total Maintenance:** ${st.session_state.summary['total_maintenance']:,.0f}")
                st.write(f"**Total Property Tax:** ${st.session_state.summary['total_property_tax']:,.0f}")
                st.write(f"**Total Selling Costs:** ${st.session_state.summary['total_selling_costs']:,.0f}")
                st.write("---")
                st.write(f"**Home Appreciation:** ${st.session_state.summary['home_sale_gains']:,.0f}")
                st.write(f"**Interest Tax Savings:** ${st.session_state.summary['total_interest_tax_savings']:,.0f}")
                st.write(f"**Capital Gains Tax Savings:** ${st.session_state.summary['capital_gains_tax_savings']:,.0f}")
            
            with col2:
                st.markdown("#### 🏠 Rental Costs")
                st.write(f"**Total Rent Paid:** ${st.session_state.summary['total_rent']:,.0f}")
                if inputs['stocks_enabled']:
                    st.write(f"**Capital Gains Tax on Stocks:** ${st.session_state.summary['capital_gains_tax_owed']:,.0f}")
                st.write("---")
                if inputs['stocks_enabled']:
                    st.write(f"**Stock Investment Gains:** ${st.session_state.summary['stock_investment_gains']:,.0f}")
                st.write(f"**Standard Deduction Benefit:** ${st.session_state.summary['rental_standard_deduction_benefit']:,.0f}")

if __name__ == "__main__":
    main() 