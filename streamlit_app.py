#!/usr/bin/env python3

import streamlit as st
import pandas as pd
from home_calculator_core import HomeCalculatorCore, DEFAULT_VALUES
import copy

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
        # Initialize scenario management
        if 'scenarios' not in st.session_state:
            st.session_state.scenarios = {
                'Scenario 1': {
                    'inputs': DEFAULT_VALUES.copy(),
                    'mortgage_data': [],
                    'rent_data': [],
                    'summary': {},
                    'calculated': False
                }
            }
        if 'active_scenario' not in st.session_state:
            st.session_state.active_scenario = 'Scenario 1'
        if 'scenario_counter' not in st.session_state:
            st.session_state.scenario_counter = 1
        if 'comparison_mode' not in st.session_state:
            st.session_state.comparison_mode = False
            
        # Legacy support
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
    
    def add_scenario(self):
        """Add a new scenario"""
        st.session_state.scenario_counter += 1
        new_scenario_name = f"Scenario {st.session_state.scenario_counter}"
        st.session_state.scenarios[new_scenario_name] = {
            'inputs': DEFAULT_VALUES.copy(),
            'mortgage_data': [],
            'rent_data': [],
            'summary': {},
            'calculated': False
        }
        st.session_state.active_scenario = new_scenario_name
        self.sync_legacy_session_state()
        return new_scenario_name
    
    def delete_scenario(self, scenario_name):
        """Delete a scenario"""
        if len(st.session_state.scenarios) > 1 and scenario_name in st.session_state.scenarios:
            del st.session_state.scenarios[scenario_name]
            # Switch to first available scenario
            st.session_state.active_scenario = list(st.session_state.scenarios.keys())[0]
            self.sync_legacy_session_state()
    
    def rename_scenario(self, old_name, new_name):
        """Rename a scenario"""
        if old_name in st.session_state.scenarios and new_name not in st.session_state.scenarios:
            st.session_state.scenarios[new_name] = st.session_state.scenarios.pop(old_name)
            if st.session_state.active_scenario == old_name:
                st.session_state.active_scenario = new_name
    
    def get_current_scenario(self):
        """Get the current active scenario data"""
        return st.session_state.scenarios[st.session_state.active_scenario]
    
    def update_scenario_inputs(self, inputs):
        """Update inputs for the current scenario"""
        st.session_state.scenarios[st.session_state.active_scenario]['inputs'] = inputs
    
    def update_scenario_results(self, mortgage_data, rent_data, summary):
        """Update results for the current scenario"""
        current_scenario = st.session_state.scenarios[st.session_state.active_scenario]
        current_scenario['mortgage_data'] = mortgage_data
        current_scenario['rent_data'] = rent_data
        current_scenario['summary'] = summary
        current_scenario['calculated'] = True
    
    def sync_legacy_session_state(self):
        """Sync legacy session state with current scenario data"""
        current_scenario = self.get_current_scenario()
        if current_scenario['calculated']:
            st.session_state.mortgage_data = current_scenario['mortgage_data']
            st.session_state.rent_data = current_scenario['rent_data']
            st.session_state.summary = current_scenario['summary']
            st.session_state.calculated = True
        else:
            st.session_state.calculated = False
    
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
    
    calculator = HomeCalculator()
    
    # Scenario Management Header
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        # Scenario Tabs
        scenario_names = list(st.session_state.scenarios.keys())
        
        # Create tabs for scenarios
        if len(scenario_names) > 1:
            selected_tab = st.radio("", scenario_names, horizontal=True, key="scenario_selector")
        else:
            selected_tab = scenario_names[0]
            st.write(f"**{selected_tab}**")
        
        # Update active scenario and sync data if it changed
        if st.session_state.active_scenario != selected_tab:
            st.session_state.active_scenario = selected_tab
            calculator.sync_legacy_session_state()
    
    with col2:
        if st.button("➕ Add Scenario"):
            calculator.add_scenario()
            st.rerun()
    
    with col3:
        if len(st.session_state.scenarios) > 1:
            if st.button("🗑️ Delete"):
                calculator.delete_scenario(st.session_state.active_scenario)
                st.rerun()
    
    with col4:
        comparison_mode = st.toggle("Compare All", value=st.session_state.comparison_mode)
        st.session_state.comparison_mode = comparison_mode
    
    st.markdown("---")
    
    # Get current scenario data and sync legacy session state
    current_scenario = calculator.get_current_scenario()
    current_inputs = current_scenario['inputs']
    calculator.sync_legacy_session_state()
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("📊 Input Parameters")
        
        # General Settings
        st.subheader("⏱️ General Settings")
        years = st.number_input("Number of Years to Compare", min_value=1, max_value=50, value=current_inputs['years'])
        
        # Home Purchase Details
        st.subheader("🏠 Home Purchase Details")
        home_price = st.number_input("Home Price ($)", min_value=50000, max_value=10000000, value=current_inputs['home_price'], step=10000)
        down_payment_pct = st.number_input("Down Payment (%)", min_value=0.0, max_value=100.0, value=current_inputs['down_payment_pct'], step=0.5)
        apr = st.number_input("30-Year Fixed APR (%)", min_value=0.1, max_value=20.0, value=current_inputs['apr'], step=0.01)
        property_tax_rate = st.number_input("Property Tax (% per year)", min_value=0.0, max_value=10.0, value=current_inputs['property_tax_rate'], step=0.01)
        property_tax_growth = st.number_input("Property Tax Growth (% per year, CA Prop 13 = 2%)", min_value=0.0, max_value=10.0, value=current_inputs.get('property_tax_growth', 2.0), step=0.01)
        house_growth = st.number_input("House Price Growth (% per year)", min_value=-10.0, max_value=50.0, value=current_inputs['house_growth'], step=0.1)
        maintenance_annual = st.number_input("Maintenance Expense Annual ($)", min_value=0, max_value=100000, value=current_inputs['maintenance_annual'], step=500)
        brokerage_cost = st.number_input("Brokerage Cost (% of sale price)", min_value=0.0, max_value=20.0, value=current_inputs['brokerage_cost'], step=0.1)
        registration_cost = st.number_input("Registration Expenses (% of purchase price)", min_value=0.0, max_value=10.0, value=current_inputs['registration_cost'], step=0.1)
        capital_gains_exemption_enabled = st.checkbox("Include Capital Gains Tax Benefit on Home Growth", value=current_inputs['capital_gains_exemption_enabled'])
        
        # Rental Details
        st.subheader("🏠 Rental Details")
        monthly_rent = st.number_input("Monthly Rent ($)", min_value=500, max_value=50000, value=current_inputs['monthly_rent'], step=50)
        rent_growth = st.number_input("Rent Growth (% per year)", min_value=0.0, max_value=20.0, value=current_inputs['rent_growth'], step=0.1)
        
        # Income & Tax Details
        st.subheader("💰 Income & Tax Details")
        monthly_income = st.number_input("Monthly Income ($)", min_value=1000, max_value=200000, value=current_inputs['monthly_income'], step=500)
        income_growth = st.number_input("Monthly Income Growth (% per year)", min_value=0.0, max_value=50.0, value=current_inputs['income_growth'], step=0.1)
        rsu_income = st.number_input("RSUs Income Supplement ($)", min_value=0, max_value=1000000, value=current_inputs['rsu_income'], step=1000)
        tax_rate = st.number_input("IRS Max Tax Slab (%)", min_value=0.0, max_value=50.0, value=current_inputs['tax_rate'], step=0.5)
        standard_deduction = st.number_input("Standard Deduction ($)", min_value=0, max_value=100000, value=current_inputs['standard_deduction'], step=1000)
        
        # Stock Investment Settings
        st.subheader("📈 Stock Investment Settings")
        stocks_enabled = st.checkbox("Enable Stock Investment Analysis", value=current_inputs['stocks_enabled'])
        if stocks_enabled:
            include_down_payment_growth = st.checkbox("Include Down Payment Growth", value=current_inputs['include_down_payment_growth'])
            stock_growth = st.number_input("Stock Market Growth (% per year)", min_value=0.0, max_value=50.0, value=current_inputs['stock_growth'], step=0.1)
            capital_gains_tax_rate = st.number_input("Capital Gains Tax Rate (%)", min_value=0.0, max_value=50.0, value=current_inputs['capital_gains_tax_rate'], step=0.5)
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
    
    # Update current scenario inputs
    calculator.update_scenario_inputs(inputs)
    
    # Generate Analysis Button
    if st.button("🚀 Generate Comparison", type="primary", use_container_width=True):
        with st.spinner("Calculating financial analysis..."):
            mortgage_data, rent_data, summary = calculator.generate_analysis(inputs)
            calculator.update_scenario_results(mortgage_data, rent_data, summary)
            # Update legacy session state for backward compatibility
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
                st.write(f"**Brokerage Costs (+):** ${st.session_state.summary['brokerage_costs']:,.0f}")
                st.write(f"**Registration Costs (+):** ${st.session_state.summary['registration_costs']:,.0f}")
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
    
    # Comparison Mode
    if st.session_state.comparison_mode and len(st.session_state.scenarios) > 1:
        st.markdown("---")
        st.markdown("## 📊 Scenario Comparison")
        
        # Prepare comparison data
        comparison_data = []
        for scenario_name, scenario_data in st.session_state.scenarios.items():
            if scenario_data['calculated']:
                summary = scenario_data['summary']
                comparison_data.append({
                    'Scenario': scenario_name,
                    'Ownership Net Cost': f"${summary['ownership_net_cost']:,.0f}",
                    'Rental Net Cost': f"${summary['rent_net_cost']:,.0f}",
                    'Winner': summary['winner'],
                    'Savings': f"${summary['savings']:,.0f}",
                    'Home Price': f"${scenario_data['inputs']['home_price']:,.0f}",
                    'Monthly Rent': f"${scenario_data['inputs']['monthly_rent']:,.0f}",
                    'Down Payment': f"{scenario_data['inputs']['down_payment_pct']:.1f}%",
                    'APR': f"{scenario_data['inputs']['apr']:.2f}%"
                })
        
        if comparison_data:
            df = pd.DataFrame(comparison_data)
            st.dataframe(df, use_container_width=True)
            
            # Summary stats
            st.markdown("### 📈 Quick Insights")
            ownership_costs = [scenario['summary']['ownership_net_cost'] for scenario in st.session_state.scenarios.values() if scenario['calculated']]
            rental_costs = [scenario['summary']['rent_net_cost'] for scenario in st.session_state.scenarios.values() if scenario['calculated']]
            
            if ownership_costs and rental_costs:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Ownership Range", f"${min(ownership_costs):,.0f} - ${max(ownership_costs):,.0f}")
                with col2:
                    st.metric("Rental Range", f"${min(rental_costs):,.0f} - ${max(rental_costs):,.0f}")
                with col3:
                    avg_savings = sum([scenario['summary']['savings'] for scenario in st.session_state.scenarios.values() if scenario['calculated']]) / len(comparison_data)
                    st.metric("Avg Savings", f"${avg_savings:,.0f}")
        else:
            st.info("💡 Generate analysis for multiple scenarios to see comparison table")

if __name__ == "__main__":
    main() 