#!/usr/bin/env python3

import streamlit as st
import pandas as pd
from home_calculator_core import HomeCalculatorCore, DEFAULT_VALUES

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
    
    def generate_analysis(self, inputs):
        """Generate the complete financial analysis using core module"""
        # Get raw data from core module
        mortgage_data_raw, rent_data_raw, summary = HomeCalculatorCore.generate_complete_analysis(inputs)
        
        # Format data for display in Streamlit tables
        mortgage_data = self._format_mortgage_data(mortgage_data_raw)
        rent_data = self._format_rent_data(rent_data_raw, inputs['stocks_enabled'])
        
        return mortgage_data, rent_data, summary
    
    def _format_mortgage_data(self, raw_data):
        """Format mortgage data for display"""
        formatted_data = []
        for row in raw_data:
            formatted_data.append({
                'Year': row['Year'],
                'Monthly EMI': f"${row['Monthly EMI']:,.2f}",
                'Principal Paid': f"${row['Principal Paid']:,.2f}",
                'Interest Paid': f"${row['Interest Paid']:,.2f}",
                'Deductible Interest': f"${row['Deductible Interest']:,.2f}",
                'Interest Tax Savings': f"${row['Interest Tax Savings']:,.2f}",
                'Total P&I': f"${row['Total P&I']:,.2f}",
                'Property Tax': f"${row['Property Tax']:,.2f}",
                'Remaining Balance': f"${row['Remaining Balance']:,.2f}",
                'Home Value': f"${row['Home Value']:,.2f}"
            })
        return formatted_data
    
    def _format_rent_data(self, raw_data, stocks_enabled):
        """Format rent data for display"""
        formatted_data = []
        for row in raw_data:
            formatted_row = {
                'Year': row['Year'],
                'Monthly Rent': f"${row['Monthly Rent']:,.2f}",
                'Annual Rent': f"${row['Annual Rent']:,.2f}",
                'EMI-Rent Diff': f"${row['EMI-Rent Diff']:,.2f}",
                'Yearly Savings with EMI-Rent Diff': f"${row['Yearly Savings with EMI-Rent Diff']:,.2f}"
            }
            
            if stocks_enabled:
                formatted_row.update({
                    'Down Payment Investment': f"${row['Down Payment Investment']:,.2f}",
                    'EMI-Rent Diff Investment': f"${row['EMI-Rent Diff Investment']:,.2f}",
                    'Total Stock Value': f"${row['Total Stock Value']:,.2f}"
                })
            
            formatted_data.append(formatted_row)
        return formatted_data

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
        years = st.number_input("Number of Years to Compare", min_value=1, max_value=50, value=DEFAULT_VALUES['years'])
        
        # Home Purchase Details
        st.subheader("🏠 Home Purchase Details")
        home_price = st.number_input("Home Price ($)", min_value=50000, max_value=10000000, value=DEFAULT_VALUES['home_price'], step=10000)
        down_payment_pct = st.number_input("Down Payment (%)", min_value=0.0, max_value=100.0, value=DEFAULT_VALUES['down_payment_pct'], step=0.5)
        apr = st.number_input("30-Year Fixed APR (%)", min_value=0.1, max_value=20.0, value=DEFAULT_VALUES['apr'], step=0.01)
        property_tax_rate = st.number_input("Property Tax (% per year)", min_value=0.0, max_value=10.0, value=DEFAULT_VALUES['property_tax_rate'], step=0.01)
        property_tax_growth = st.number_input("Property Tax Growth (% per year, CA Prop 13 = 2%)", min_value=0.0, max_value=10.0, value=DEFAULT_VALUES.get('property_tax_growth', 2.0), step=0.01)
        house_growth = st.number_input("House Price Growth (% per year)", min_value=-10.0, max_value=50.0, value=DEFAULT_VALUES['house_growth'], step=0.1)
        maintenance_annual = st.number_input("Maintenance Expense Annual ($)", min_value=0, max_value=100000, value=DEFAULT_VALUES['maintenance_annual'], step=500)
        brokerage_cost = st.number_input("Brokerage Cost (% of sale price)", min_value=0.0, max_value=20.0, value=DEFAULT_VALUES['brokerage_cost'], step=0.1)
        registration_cost = st.number_input("Registration Expenses (% of sale price)", min_value=0.0, max_value=10.0, value=DEFAULT_VALUES['registration_cost'], step=0.1)
        capital_gains_exemption_enabled = st.checkbox("Include Capital Gains Tax Benefit on Home Growth", value=DEFAULT_VALUES['capital_gains_exemption_enabled'])
        
        # Rental Details
        st.subheader("🏠 Rental Details")
        monthly_rent = st.number_input("Monthly Rent ($)", min_value=500, max_value=50000, value=DEFAULT_VALUES['monthly_rent'], step=50)
        rent_growth = st.number_input("Rent Growth (% per year)", min_value=0.0, max_value=20.0, value=DEFAULT_VALUES['rent_growth'], step=0.1)
        
        # Income & Tax Details
        st.subheader("💰 Income & Tax Details")
        monthly_income = st.number_input("Monthly Income ($)", min_value=1000, max_value=200000, value=DEFAULT_VALUES['monthly_income'], step=500)
        income_growth = st.number_input("Monthly Income Growth (% per year)", min_value=0.0, max_value=50.0, value=DEFAULT_VALUES['income_growth'], step=0.1)
        rsu_income = st.number_input("RSUs Income Supplement ($)", min_value=0, max_value=1000000, value=DEFAULT_VALUES['rsu_income'], step=1000)
        tax_rate = st.number_input("IRS Max Tax Slab (%)", min_value=0.0, max_value=50.0, value=DEFAULT_VALUES['tax_rate'], step=0.5)
        standard_deduction = st.number_input("Standard Deduction ($)", min_value=0, max_value=100000, value=DEFAULT_VALUES['standard_deduction'], step=1000)
        
        # Stock Investment Settings
        st.subheader("📈 Stock Investment Settings")
        stocks_enabled = st.checkbox("Enable Stock Investment Analysis", value=DEFAULT_VALUES['stocks_enabled'])
        if stocks_enabled:
            include_down_payment_growth = st.checkbox("Include Down Payment Growth", value=DEFAULT_VALUES['include_down_payment_growth'])
            stock_growth = st.number_input("Stock Market Growth (% per year)", min_value=0.0, max_value=50.0, value=DEFAULT_VALUES['stock_growth'], step=0.1)
            capital_gains_tax_rate = st.number_input("Capital Gains Tax Rate (%)", min_value=0.0, max_value=50.0, value=DEFAULT_VALUES['capital_gains_tax_rate'], step=0.5)
        else:
            include_down_payment_growth = False
            stock_growth = 0
            capital_gains_tax_rate = 0
    
    # Collect all inputs
    inputs = {
        'years': years, 'home_price': home_price, 'down_payment_pct': down_payment_pct,
        'apr': apr, 'property_tax_rate': property_tax_rate, 'property_tax_growth': property_tax_growth, 'house_growth': house_growth,
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
                st.write(f"**Total Interest Paid (+):** ${st.session_state.summary['total_interest']:,.0f}")
                st.write(f"**Total Maintenance (+):** ${st.session_state.summary['total_maintenance']:,.0f}")
                st.write(f"**Total Property Tax (+):** ${st.session_state.summary['total_property_tax']:,.0f}")
                st.write(f"**Total Selling Costs (+):** ${st.session_state.summary['total_selling_costs']:,.0f}")
                st.write("---")
                st.write(f"**Home Appreciation (-):** ${st.session_state.summary['home_sale_gains']:,.0f}")
                st.write(f"**Interest Tax Savings (-) @ {inputs['tax_rate']:.1f}% Tax Slab:** ${st.session_state.summary['total_interest_tax_savings']:,.0f}")
                st.write(f"**Capital Gains Tax Savings (-) @ {st.session_state.summary['home_capital_gains_rate']:.1f}% LTCG:** ${st.session_state.summary['capital_gains_tax_savings']:,.0f}")
            
            with col2:
                st.markdown("#### 🏠 Rental Costs")
                st.write(f"**Total Rent Paid (+):** ${st.session_state.summary['total_rent']:,.0f}")
                if inputs['stocks_enabled']:
                    st.write(f"**Capital Gains Tax on Stocks (+):** ${st.session_state.summary['capital_gains_tax_owed']:,.0f}")
                st.write("---")
                if inputs['stocks_enabled']:
                    if inputs['include_down_payment_growth']:
                        st.write(f"**Down Payment Investment Gain (-):** ${st.session_state.summary['down_payment_investment_gain']:,.0f}")
                    st.write(f"**EMI-Rent Difference Investment Gain (-):** ${st.session_state.summary['emi_rent_diff_investment_gain']:,.0f}")
                    st.write(f"**Total Stock Investment Gains (-):** ${st.session_state.summary['stock_investment_gains']:,.0f}")
                st.write(f"**Standard Deduction Benefit (-) @ {inputs['tax_rate']:.1f}% Tax Slab:** ${st.session_state.summary['rental_standard_deduction_benefit']:,.0f}")
                
                # Add explanation section
                if inputs['stocks_enabled']:
                    st.write("---")
                    st.markdown("#### 📊 Stock Investment Calculation Details")
                    if inputs['include_down_payment_growth']:
                        down_payment = inputs['home_price'] * (inputs['down_payment_pct'] / 100)
                        st.write(f"• **Down Payment**: ${down_payment:,.0f} invested at {inputs['stock_growth']:.1f}% for {inputs['years']} years")
                        final_dp_value = down_payment * ((1 + inputs['stock_growth']/100) ** inputs['years'])
                        st.write(f"• **Grows to**: ${final_dp_value:,.0f} (gain: ${st.session_state.summary['down_payment_investment_gain']:,.0f})")
                    st.write(f"• **Monthly EMI-Rent savings** invested annually at {inputs['stock_growth']:.1f}%")
                    st.write(f"• **Total investment gains**: ${st.session_state.summary['stock_investment_gains']:,.0f}")
                    st.write(f"• **Capital gains tax** ({inputs['capital_gains_tax_rate']:.1f}%): ${st.session_state.summary['capital_gains_tax_owed']:,.0f}")

if __name__ == "__main__":
    main() 