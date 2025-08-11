#!/Library/Frameworks/Python.framework/Versions/3.13/bin/python3

import tkinter as tk
from tkinter import ttk, messagebox
from home_calculator_core import DEFAULT_VALUES
from tkinter import font

class HomeRentCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Home Ownership vs Rent Calculator")
        self.root.geometry("1400x1080")
        self.root.minsize(1200, 900)
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Create main container
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(2, weight=1)  # Result frame is now in column 2
        main_frame.rowconfigure(1, weight=1)     # Input/result row expands to fill space
        
        # Title
        title_font = font.Font(family="Arial", size=16, weight="bold")
        title_label = tk.Label(main_frame, text="Home Ownership vs Rent Calculator", 
                              font=title_font, bg='#f0f0f0', fg='#2c3e50')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Create scrollable input frame
        input_canvas = tk.Canvas(main_frame, width=450, bg='#f0f0f0', highlightthickness=0)
        input_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=input_canvas.yview)
        input_frame = ttk.Frame(input_canvas)
        
        # Store references for later use
        self.input_canvas = input_canvas
        self.input_scrollbar = input_scrollbar
        
        input_canvas.configure(yscrollcommand=input_scrollbar.set)
        input_canvas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        input_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))
        
        # Create result frame
        self.result_frame = ttk.Frame(main_frame)
        self.result_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.create_input_widgets(input_frame)
        
        # Configure scrollable area
        input_frame.update_idletasks()
        input_canvas.create_window((0, 0), window=input_frame, anchor="nw")
        input_canvas.configure(scrollregion=input_canvas.bbox("all"))
        
        # Bind mouse wheel to canvas for scrolling
        def _on_mousewheel(event):
            input_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def _bind_to_mousewheel(event):
            input_canvas.bind_all("<MouseWheel>", _on_mousewheel)
            input_canvas.bind_all("<Button-4>", lambda e: input_canvas.yview_scroll(-1, "units"))
            input_canvas.bind_all("<Button-5>", lambda e: input_canvas.yview_scroll(1, "units"))
        
        def _unbind_from_mousewheel(event):
            input_canvas.unbind_all("<MouseWheel>")
            input_canvas.unbind_all("<Button-4>")
            input_canvas.unbind_all("<Button-5>")
        
        input_canvas.bind('<Enter>', _bind_to_mousewheel)
        input_canvas.bind('<Leave>', _unbind_from_mousewheel)
        
        # Update scroll region when the frame size changes
        def _configure_scroll_region(event=None):
            input_canvas.configure(scrollregion=input_canvas.bbox("all"))
        
        input_frame.bind('<Configure>', _configure_scroll_region)
        
        self.create_result_widgets()
        
        # Reset scroll to top
        input_canvas.yview_moveto(0)
        
    def toggle_stock_inputs(self):
        """Enable/disable stock input widgets based on checkbox state"""
        state = 'normal' if self.enable_stocks.get() else 'disabled'
        for widget in self.stock_widgets:
            if isinstance(widget, (ttk.Entry, ttk.Checkbutton)):
                widget.config(state=state)
        
    def create_input_widgets(self, parent):
        # General inputs
        general_frame = ttk.LabelFrame(parent, text="General Settings", padding="10")
        general_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(general_frame, text="Number of Years to Compare:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.years_entry = ttk.Entry(general_frame, width=15)
        self.years_entry.insert(0, "5")
        self.years_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        
        # Purchase Group
        purchase_frame = ttk.LabelFrame(parent, text="Home Purchase Details", padding="10")
        purchase_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        purchase_inputs = [
            ("Home Price ($):", "home_price", str(DEFAULT_VALUES['home_price'])),
            ("Down Payment (%):", "down_payment_pct", "20"),
            ("30-Year Fixed APR (%):", "apr", "5.75"),
            ("Property Tax (% per year):", "property_tax", str(DEFAULT_VALUES['property_tax_rate'])),
            ("House Price Growth (% per year):", "house_growth", "3.0"),
            ("Maintenance Expense Annual ($):", "maintenance_annual", "10000"),
            ("Brokerage Cost (% of sale price):", "brokerage_cost", "6.0"),
            ("Registration Expenses (% of sale price):", "registration_cost", "2.0")
        ]
        
        self.purchase_entries = {}
        for i, (label, key, default) in enumerate(purchase_inputs):
            ttk.Label(purchase_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(purchase_frame, width=15)
            entry.insert(0, default)
            entry.grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=2)
            self.purchase_entries[key] = entry
        
        # Capital gains tax exemption checkbox
        self.enable_capital_gains_exemption = tk.BooleanVar(value=True)
        capital_gains_checkbox = ttk.Checkbutton(purchase_frame, 
                                                text="Include Capital Gains Tax Benefit on Home Growth", 
                                                variable=self.enable_capital_gains_exemption)
        capital_gains_checkbox.grid(row=len(purchase_inputs), column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Rent Group
        rent_frame = ttk.LabelFrame(parent, text="Rental Details", padding="10")
        rent_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        rent_inputs = [
            ("Monthly Rent ($):", "monthly_rent", str(DEFAULT_VALUES['monthly_rent'])),
            ("Rent Growth (% per year):", "rent_growth", str(DEFAULT_VALUES['rent_growth']))
        ]
        
        self.rent_entries = {}
        for i, (label, key, default) in enumerate(rent_inputs):
            ttk.Label(rent_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(rent_frame, width=15)
            entry.insert(0, default)
            entry.grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=2)
            self.rent_entries[key] = entry
        
        # Income Group
        income_frame = ttk.LabelFrame(parent, text="Income & Tax Details", padding="10")
        income_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        income_inputs = [
            ("Monthly Income ($):", "monthly_income", "8000"),
            ("Monthly Income Growth (% per year):", "income_growth", "4.0"),
            ("RSUs Income Supplement ($):", "rsu_income", "0"),
            ("IRS Max Tax Slab (%):", "tax_rate", "35"),
            ("Standard Deduction ($):", "standard_deduction", "0")
        ]
        
        self.income_entries = {}
        for i, (label, key, default) in enumerate(income_inputs):
            ttk.Label(income_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(income_frame, width=15)
            entry.insert(0, default)
            entry.grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=2)
            self.income_entries[key] = entry
        
        # Stock Investment Group
        stock_frame = ttk.LabelFrame(parent, text="Stock Investment Settings", padding="10")
        stock_frame.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Stock investment checkbox
        self.enable_stocks = tk.BooleanVar(value=True)
        stocks_checkbox = ttk.Checkbutton(stock_frame, text="Enable Stock Investment Analysis", 
                                         variable=self.enable_stocks, command=self.toggle_stock_inputs)
        stocks_checkbox.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Down payment growth checkbox
        self.include_down_payment_growth = tk.BooleanVar(value=True)
        down_payment_growth_checkbox = ttk.Checkbutton(stock_frame, text="Include Down Payment Growth", 
                                                      variable=self.include_down_payment_growth)
        down_payment_growth_checkbox.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        stock_inputs = [
            ("Stock Market Growth (% per year):", "stock_growth", "8"),
            ("Capital Gains Tax Rate (%):", "capital_gains_tax", "20")
        ]
        
        self.stock_entries = {}
        # Store references for enabling/disabling
        if not hasattr(self, 'stock_widgets'):
            self.stock_widgets = []
        self.stock_widgets.append(down_payment_growth_checkbox)  # Add the checkbox to widgets list
        
        for i, (label, key, default) in enumerate(stock_inputs, start=2):  # Start at row 2 now
            stock_label = ttk.Label(stock_frame, text=label)
            stock_label.grid(row=i, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(stock_frame, width=15)
            entry.insert(0, default)
            entry.grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=2)
            self.stock_entries[key] = entry
            
            self.stock_widgets.extend([stock_label, entry])
        
        # Generate button
        generate_btn = ttk.Button(parent, text="Generate Comparison", 
                                 command=self.generate_comparison, style='Accent.TButton')
        generate_btn.grid(row=5, column=0, pady=20)
        
    def create_result_widgets(self):
        # Results title
        result_title = tk.Label(self.result_frame, text="Comparison Results", 
                               font=font.Font(family="Arial", size=14, weight="bold"),
                               bg='#f0f0f0', fg='#2c3e50')
        result_title.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.result_frame)
        self.notebook.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for result frame
        self.result_frame.columnconfigure(0, weight=1)
        self.result_frame.rowconfigure(1, weight=1)
        
    def calculate_mortgage_payment(self, principal, annual_rate, years):
        """Calculate monthly mortgage payment using standard formula"""
        monthly_rate = annual_rate / 100 / 12
        num_payments = years * 12
        
        if monthly_rate == 0:
            return principal / num_payments
        
        payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
                 ((1 + monthly_rate)**num_payments - 1)
        return payment
    
    def generate_comparison(self):
        try:
            # Get all input values
            years = int(self.years_entry.get())
            
            # Purchase inputs
            home_price = float(self.purchase_entries['home_price'].get())
            down_payment_pct = float(self.purchase_entries['down_payment_pct'].get())
            down_payment = home_price * (down_payment_pct / 100)
            apr = float(self.purchase_entries['apr'].get())
            property_tax_rate = float(self.purchase_entries['property_tax'].get())
            house_growth = float(self.purchase_entries['house_growth'].get())
            maintenance_annual = float(self.purchase_entries['maintenance_annual'].get())
            brokerage_cost = float(self.purchase_entries['brokerage_cost'].get())
            registration_cost = float(self.purchase_entries['registration_cost'].get())
            
            # Rent inputs
            monthly_rent = float(self.rent_entries['monthly_rent'].get())
            rent_growth = float(self.rent_entries['rent_growth'].get())
            
            # Income inputs
            monthly_income = float(self.income_entries['monthly_income'].get())
            income_growth = float(self.income_entries['income_growth'].get())
            rsu_income = float(self.income_entries['rsu_income'].get())
            tax_rate = float(self.income_entries['tax_rate'].get())
            standard_deduction = float(self.income_entries['standard_deduction'].get())
            
            # Stock investment inputs
            stocks_enabled = self.enable_stocks.get()
            stock_growth = float(self.stock_entries['stock_growth'].get()) if stocks_enabled else 0
            capital_gains_tax_rate = float(self.stock_entries['capital_gains_tax'].get()) if stocks_enabled else 0
            include_down_payment_growth = self.include_down_payment_growth.get() if stocks_enabled else False
            
            # Capital gains exemption input
            capital_gains_exemption_enabled = self.enable_capital_gains_exemption.get()
            
            # Calculate loan amount
            loan_amount = home_price - down_payment
            
            # Calculate monthly mortgage payment (principal + interest)
            monthly_payment = self.calculate_mortgage_payment(loan_amount, apr, 30)
            
            # Calculate property tax monthly
            annual_property_tax = home_price * (property_tax_rate / 100)
            monthly_property_tax = annual_property_tax / 12
            
            # Generate year-by-year data
            self.generate_detailed_analysis(years, monthly_payment, monthly_rent, 
                                          rent_growth, monthly_property_tax, 
                                          home_price, house_growth, loan_amount, apr,
                                          down_payment, stock_growth, property_tax_rate, tax_rate, stocks_enabled, standard_deduction,
                                          brokerage_cost, registration_cost, capital_gains_exemption_enabled, maintenance_annual,
                                          include_down_payment_growth, capital_gains_tax_rate)
            
        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter valid numeric values for all fields.")
        except Exception as e:
            messagebox.showerror("Calculation Error", f"An error occurred: {str(e)}")
    
    def generate_detailed_analysis(self, years, monthly_payment, initial_rent, 
                                 rent_growth, monthly_property_tax, initial_home_value, 
                                 house_growth, loan_amount, apr, down_payment, stock_growth, property_tax_rate, tax_rate, stocks_enabled, standard_deduction,
                                 brokerage_cost, registration_cost, capital_gains_exemption_enabled, maintenance_annual,
                                 include_down_payment_growth, capital_gains_tax_rate):
        # Clear previous results
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
        
        # Create mortgage amortization table
        mortgage_data = []
        current_balance = loan_amount
        monthly_rate = apr / 100 / 12
        
        for year in range(1, years + 1):
            year_principal = 0
            year_interest = 0
            
            for month in range(12):
                if current_balance > 0:
                    interest_payment = current_balance * monthly_rate
                    principal_payment = monthly_payment - interest_payment
                    
                    year_interest += interest_payment
                    year_principal += principal_payment
                    current_balance -= principal_payment
                    
                    if current_balance < 0:
                        current_balance = 0
            
            # Calculate property tax for this year
            current_home_value = initial_home_value * ((1 + house_growth/100) ** year)
            annual_property_tax = current_home_value * (property_tax_rate / 100)
            
            # Property tax is only an expense, no tax benefit
            
            # Calculate mortgage interest deduction (limited to $750k principal per IRS)
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
        
        # Create rent table with conditional stock investment calculations
        rent_data = []
        current_rent = initial_rent
        cumulative_emi_rent_diff_investment = 0  # Cumulative investment balance
        
        for year in range(1, years + 1):
            annual_rent = current_rent * 12
            monthly_emi_rent_diff = monthly_payment - current_rent  # Can be positive or negative
            annual_emi_rent_diff = monthly_emi_rent_diff * 12
            monthly_emi_rent_diff_positive = max(0, monthly_emi_rent_diff)  # Only positive for investments
            annual_emi_rent_diff_positive = monthly_emi_rent_diff_positive * 12
            
            if stocks_enabled:
                # Calculate stock growth on down payment (only if enabled)
                if include_down_payment_growth:
                    down_payment_value = down_payment * ((1 + stock_growth/100) ** year)
                else:
                    down_payment_value = down_payment  # No growth, just original amount
                
                # Calculate stock growth on accumulated EMI-rent difference investments
                if year == 1:
                    cumulative_emi_rent_diff_investment = annual_emi_rent_diff_positive
                else:
                    # Previous year's investment grows + new year's investment
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
                # No stock investments - simplified rent table
                rent_data.append({
                    'Year': year,
                    'Monthly Rent': f"${current_rent:,.2f}",
                    'Annual Rent': f"${annual_rent:,.2f}",
                    'EMI-Rent Diff': f"${monthly_emi_rent_diff:,.2f}",
                    'Yearly Savings with EMI-Rent Diff': f"${annual_emi_rent_diff:,.2f}"
                })
            
            current_rent *= (1 + rent_growth/100)
        
        # Create tabs
        try:
            self.create_mortgage_tab(mortgage_data)
            self.create_rent_tab(rent_data, stocks_enabled)
            self.create_summary_tab(mortgage_data, rent_data, years, monthly_payment, down_payment, stocks_enabled, property_tax_rate, tax_rate, standard_deduction,
                                   brokerage_cost, registration_cost, capital_gains_exemption_enabled, maintenance_annual,
                                   include_down_payment_growth, capital_gains_tax_rate)
            
            # Switch to Summary tab by default
            self.notebook.select(2)  # Summary is the 3rd tab (index 2)
        except Exception as e:
            messagebox.showerror("Calculation Error", f"Error creating results: {str(e)}")
            print(f"Debug - Error in creating tabs: {e}")
            print(f"Debug - Mortgage data length: {len(mortgage_data)}")
            print(f"Debug - Rent data length: {len(rent_data)}")
            if rent_data:
                print(f"Debug - First rent data: {rent_data[0]}")
                print(f"Debug - Last rent data: {rent_data[-1]}")
    
    def create_mortgage_tab(self, data):
        # Create mortgage tab
        mortgage_frame = ttk.Frame(self.notebook)
        self.notebook.add(mortgage_frame, text="Mortgage Details")
        
        # Create treeview for mortgage data
        columns = ('Year', 'Monthly EMI', 'Principal Paid', 'Interest Paid', 'Deductible Interest', 
                  'Interest Tax Savings', 'Total P&I', 'Property Tax', 
                  'Remaining Balance', 'Home Value')
        
        mortgage_tree = ttk.Treeview(mortgage_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            mortgage_tree.heading(col, text=col)
            if col == 'Year':
                mortgage_tree.column(col, width=50, anchor='center')
            else:
                mortgage_tree.column(col, width=90, anchor='center')
        
        # Insert data
        for row in data:
            mortgage_tree.insert('', 'end', values=list(row.values()))
        
        # Add scrollbar
        scrollbar1 = ttk.Scrollbar(mortgage_frame, orient='vertical', command=mortgage_tree.yview)
        mortgage_tree.configure(yscrollcommand=scrollbar1.set)
        
        mortgage_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar1.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        mortgage_frame.columnconfigure(0, weight=1)
        mortgage_frame.rowconfigure(0, weight=1)
    
    def create_rent_tab(self, data, stocks_enabled):
        # Create rent tab
        rent_frame = ttk.Frame(self.notebook)
        self.notebook.add(rent_frame, text="Rent Details")
        
        # Create treeview for rent data with conditional columns
        if stocks_enabled:
            columns = ('Year', 'Monthly Rent', 'Annual Rent', 'EMI-Rent Diff', 'Yearly Savings with EMI-Rent Diff',
                      'Down Payment Investment', 'EMI-Rent Diff Investment', 'Total Stock Value')
        else:
            columns = ('Year', 'Monthly Rent', 'Annual Rent', 'EMI-Rent Diff', 'Yearly Savings with EMI-Rent Diff')
        
        rent_tree = ttk.Treeview(rent_frame, columns=columns, show='headings', height=15)
        
        # Define headings
        for col in columns:
            rent_tree.heading(col, text=col)
            if col == 'Year':
                rent_tree.column(col, width=50, anchor='center')
            elif col == 'Yearly Savings with EMI-Rent Diff':
                rent_tree.column(col, width=180, anchor='center')
            else:
                rent_tree.column(col, width=120, anchor='center')
        
        # Insert data
        for row in data:
            rent_tree.insert('', 'end', values=list(row.values()))
        
        # Add scrollbar
        scrollbar2 = ttk.Scrollbar(rent_frame, orient='vertical', command=rent_tree.yview)
        rent_tree.configure(yscrollcommand=scrollbar2.set)
        
        rent_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar2.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        rent_frame.columnconfigure(0, weight=1)
        rent_frame.rowconfigure(0, weight=1)
    
    def create_summary_tab(self, mortgage_data, rent_data, years, monthly_payment, down_payment, stocks_enabled, property_tax_rate, tax_rate, standard_deduction,
                          brokerage_cost, registration_cost, capital_gains_exemption_enabled, maintenance_annual,
                          include_down_payment_growth, capital_gains_tax_rate):
        # Create summary tab
        summary_frame = ttk.Frame(self.notebook)
        self.notebook.add(summary_frame, text="Summary")
        
        # Calculate totals for ownership
        total_principal = sum([float(row['Principal Paid'].replace('$', '').replace(',', '')) 
                             for row in mortgage_data])
        total_interest = sum([float(row['Interest Paid'].replace('$', '').replace(',', '')) 
                            for row in mortgage_data])
        total_property_tax = sum([float(row['Property Tax'].replace('$', '').replace(',', '')) 
                                for row in mortgage_data])
        # Property tax is only an expense, no tax savings
        total_interest_tax_savings = sum([float(row['Interest Tax Savings'].replace('$', '').replace(',', '')) 
                                        for row in mortgage_data])
        total_deductible_interest = sum([float(row['Deductible Interest'].replace('$', '').replace(',', '')) 
                                       for row in mortgage_data])
        
        # Calculate totals for rental + investments
        total_rent = sum([float(row['Annual Rent'].replace('$', '').replace(',', '')) 
                         for row in rent_data])
        
        # Get final values
        final_home_value = float(mortgage_data[-1]['Home Value'].replace('$', '').replace(',', ''))
        
        # Calculate pure home appreciation and selling costs separately
        initial_home_value = float(mortgage_data[0]['Home Value'].replace('$', '').replace(',', ''))
        total_selling_costs = final_home_value * ((brokerage_cost + registration_cost) / 100)
        net_sale_proceeds = final_home_value - total_selling_costs
        
        # Pure home growth (appreciation only)
        home_sale_gains = final_home_value - initial_home_value
        
        # Net gains after selling costs (for capital gains tax calculation)
        net_home_gains_after_costs = net_sale_proceeds - initial_home_value
        
        # Calculate capital gains tax benefit (tax saved on home growth)
        # Use long-term capital gains tax rate, not ordinary income tax rate
        home_capital_gains_rate = capital_gains_tax_rate if capital_gains_tax_rate > 0 else 20.0  # Default 20% if not set
        if capital_gains_exemption_enabled and home_sale_gains > 0:
            # Tax benefit = long_term_capital_gains_rate * growth_value (pure appreciation)
            capital_gains_tax_savings = home_sale_gains * (home_capital_gains_rate / 100)
        else:
            capital_gains_tax_savings = 0
        
        # Conditional stock calculations
        if stocks_enabled:
            # Get final values from last year data
            final_down_payment_value = float(rent_data[-1]['Down Payment Investment'].replace('$', '').replace(',', ''))
            final_emi_rent_diff_investment = float(rent_data[-1]['EMI-Rent Diff Investment'].replace('$', '').replace(',', ''))
            
            # Calculate gains using empirical formula
            # Gains from renting = down_payment_value_gain + EMI_rent_investments_value_gain
            
            # Down payment gains (only if growth enabled)
            if include_down_payment_growth:
                down_payment_value_gain = final_down_payment_value - down_payment
            else:
                down_payment_value_gain = 0  # No growth, no gains
            
            # EMI-rent difference investment gains
            total_emi_rent_diff_invested = sum([
                max(0, monthly_payment * 12 - float(row['Annual Rent'].replace('$', '').replace(',', '')))
                for row in rent_data
            ])
            emi_rent_investments_value_gain = final_emi_rent_diff_investment - total_emi_rent_diff_invested
            
            # Total stock investment gains = down_payment_value_gain + EMI_rent_investments_value_gain
            stock_investment_gains = down_payment_value_gain + emi_rent_investments_value_gain
            
            # Calculate capital gains tax on stock gains
            capital_gains_tax_owed = stock_investment_gains * (capital_gains_tax_rate / 100)
        else:
            down_payment_value_gain = 0
            emi_rent_investments_value_gain = 0
            stock_investment_gains = 0
            capital_gains_tax_owed = 0
        
        # Calculate net cost of ownership (interest + property tax - home sale gains - interest tax savings)
        ownership_net_cost = total_interest + total_property_tax - home_sale_gains - total_interest_tax_savings
        
        # Calculate standard vs itemized deduction comparison
        total_itemized_deductions = total_deductible_interest  # Only mortgage interest, not property tax
        standard_deduction_total = standard_deduction * years
        
        if total_itemized_deductions > standard_deduction_total:
            deduction_advantage = "ITEMIZED"
            deduction_benefit = total_itemized_deductions - standard_deduction_total
            additional_tax_savings = deduction_benefit * (tax_rate / 100)
        else:
            deduction_advantage = "STANDARD"
            deduction_benefit = standard_deduction_total - total_itemized_deductions
            additional_tax_savings = 0
        
        # Calculate standard deduction benefits for rental scenario
        rental_standard_deduction_benefit = standard_deduction * years * (tax_rate / 100)
        
        # Calculate detailed costs for comparison
        total_maintenance = maintenance_annual * years
        rent_net_cost = total_rent + (capital_gains_tax_owed if stocks_enabled else 0) - (stock_investment_gains if stocks_enabled else 0) - rental_standard_deduction_benefit
        # For ownership: costs (interest + maintenance + property tax + selling) minus savings (tax benefits + pure home appreciation)
        ownership_net_cost_detailed = total_interest + total_maintenance + total_property_tax + total_selling_costs - (total_interest_tax_savings + capital_gains_tax_savings) - home_sale_gains
        
        # Determine which is better
        if ownership_net_cost_detailed < rent_net_cost:
            advantage = "OWNERSHIP"
            savings = rent_net_cost - ownership_net_cost_detailed
        else:
            advantage = "RENTING"
            savings = ownership_net_cost_detailed - rent_net_cost
        
        # Calculate EMI-Rent difference savings/costs
        total_emi_payments = monthly_payment * 12 * years
        total_emi_rent_diff = total_emi_payments - total_rent
        
        # Create structured summary matching the layout
        summary_text = f"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         HOME RENT vs HOME OWNERSHIP COST                     ║
║                                ({years} YEAR ANALYSIS)                       ║
╚═══════════════════════════════════════════════════════════════════════════════╝

┌───────────────────────────────────┬───────────────────────────────────────────┐
│            HOME RENT              │          HOME OWNERSHIP COST              │
├───────────────────────────────────┼───────────────────────────────────────────┤
│                                   │                                           │
│  EXPENSES:                        │  EXPENSES:                                │
│  ① Rent Growth (+)                │  ① Interest Paid (+)                     │
│     ${total_rent:>20,.0f}         │     ${total_interest:>20,.0f}             │"""
        
        # Add capital gains tax line conditionally for rent side
        if stocks_enabled:
            summary_text += f"""
│  ② Capital Gains Tax on Stocks (+) │  ② Maintenance (Annual) (+)             │
│     ${capital_gains_tax_owed:>20,.0f}         │     ${total_maintenance:>20,.0f}          │"""
        else:
            summary_text += f"""
│                                   │  ② Maintenance (Annual) (+)              │
│                                   │     ${total_maintenance:>20,.0f}          │"""
        
        summary_text += f"""
│                                   │  ③ Property Tax (+)                      │
│                                   │     ${total_property_tax:>20,.0f}         │
│                                   │  ④ Buy/Sell Costs (+)                    │
│                                   │     ${total_selling_costs:>20,.0f}        │
│                                   │                                           │
│  SAVINGS:                         │  INCOME:                                  │"""

        if stocks_enabled:
            summary_text += f"""
│  ① EMI-Rent Difference (-)       │  ① Tax Deductions @ {tax_rate:.1f}% (-)       │
│     ${abs(total_emi_rent_diff):>20,.0f}      │     ${total_interest_tax_savings:>20,.0f}         │
│  ② Growth if Invested in Stocks (-) │  ② Home Growth (-)                     │
│     ${stock_investment_gains:>20,.0f}        │     ${home_sale_gains:>20,.0f}           │
│  ③ Standard Deduction @ {tax_rate:.1f}% (-) │                                          │
│     ${rental_standard_deduction_benefit:>20,.0f}        │                                           │"""
        else:
            summary_text += f"""
│  ① EMI-Rent Difference (-)       │  ① Tax Deductions @ {tax_rate:.1f}% (-)       │
│     ${abs(total_emi_rent_diff):>20,.0f}      │     ${total_interest_tax_savings:>20,.0f}         │
│  ② No Stock Investment (-)       │  ② Home Growth (-)                       │
│     ${0:>20,.0f}        │     ${home_sale_gains:>20,.0f}           │
│  ③ Standard Deduction @ {tax_rate:.1f}% (-) │                                          │
│     ${rental_standard_deduction_benefit:>20,.0f}        │                                           │"""
        
        # Add capital gains exemption line conditionally
        capital_gains_line = ""
        if capital_gains_exemption_enabled:
            capital_gains_line = f"""
│                                   │  ③ Capital Gains Tax Benefit (-)         │
│                                   │     (Tax Saved @ {home_capital_gains_rate:.1f}% LTCG Rate)     │
│                                   │     ${capital_gains_tax_savings:>20,.0f}         │"""
        else:
            capital_gains_line = """
│                                   │  ③ Capital Gains Tax Applied             │
│                                   │     (No Benefit Used)                    │
│                                   │                         0         │"""

        summary_text += capital_gains_line + f"""
├───────────────────────────────────┼───────────────────────────────────────────┤
│                                   │                                           │
│  NET COST:                        │  NET COST:                               │
│  ${rent_net_cost:>20,.0f}         │  ${ownership_net_cost_detailed:>20,.0f}   │
└───────────────────────────────────┴───────────────────────────────────────────┘

╔═══════════════════════════════════════════════════════════════════════════════╗
║                              COMPARISON RESULT                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

RECOMMENDED: {advantage}
SAVINGS WITH {advantage}: ${savings:,.0f}

DETAILED BREAKDOWN:
• Rent Total Cost: ${rent_net_cost:,.0f}
• Ownership Total Cost: ${ownership_net_cost_detailed:,.0f}
• Cost Difference: ${abs(rent_net_cost - ownership_net_cost_detailed):,.0f}

TAX DEDUCTION STRATEGY:
• Itemized Deductions: ${total_itemized_deductions:,.0f}
• Standard Deduction: ${standard_deduction_total:,.0f}
• Recommended: {deduction_advantage}
• Additional Tax Savings: ${additional_tax_savings:,.0f}

╔═══════════════════════════════════════════════════════════════════════════════╗
║                            NET INCOME COMPARISON                              ║
╚═══════════════════════════════════════════════════════════════════════════════╝

HOME OWNERSHIP NET INCOME:
INCOME:
• Home Appreciation: ${home_sale_gains:,.0f}
• Interest Tax Deductions: ${total_interest_tax_savings:,.0f}
• Capital Gains Tax Savings: ${capital_gains_tax_savings:,.0f}
• Total Income: ${home_sale_gains + total_interest_tax_savings + capital_gains_tax_savings:,.0f}

EXPENSES:
• Total Interest Paid: ${total_interest:,.0f}
• Total Maintenance: ${total_maintenance:,.0f}
• Total Property Taxes: ${total_property_tax:,.0f}
• Total Selling Costs: ${total_selling_costs:,.0f}
• Total Expenses: ${total_interest + total_maintenance + total_property_tax + total_selling_costs:,.0f}

NET HOME INCOME: ${(home_sale_gains + total_interest_tax_savings + capital_gains_tax_savings) - (total_interest + total_maintenance + total_property_tax + total_selling_costs):,.0f}

RENTAL + INVESTMENT NET INCOME:
INCOME:""" + (f"""
• Down Payment Growth Gains: ${down_payment_value_gain:,.0f}
• EMI-Rent Diff Investment Gains: ${emi_rent_investments_value_gain:,.0f}
• Total Stock Investment Gains: ${stock_investment_gains:,.0f}""" if stocks_enabled else """
• Stock Investment Gains: $0 (Disabled)""") + f"""
• Standard Deduction Benefit: ${rental_standard_deduction_benefit:,.0f}
• Total Income: ${(stock_investment_gains if stocks_enabled else 0) + rental_standard_deduction_benefit:,.0f}

EXPENSES:
• Total Rent Paid: ${total_rent:,.0f}""" + (f"""
• Capital Gains Tax on Stock Gains: ${capital_gains_tax_owed:,.0f}
• Total Expenses: ${total_rent + capital_gains_tax_owed:,.0f}""" if stocks_enabled else f"""
• Capital Gains Tax on Stock Gains: $0 (No Stock Gains)
• Total Expenses: ${total_rent:,.0f}""") + f"""

NET RENTAL INCOME: ${(stock_investment_gains if stocks_enabled else 0) + rental_standard_deduction_benefit - total_rent - (capital_gains_tax_owed if stocks_enabled else 0):,.0f}

NET INCOME COMPARISON:
• Home Net Income: ${(home_sale_gains + total_interest_tax_savings + capital_gains_tax_savings) - (total_interest + total_maintenance + total_property_tax + total_selling_costs):,.0f}
• Rental Net Income: ${(stock_investment_gains if stocks_enabled else 0) + rental_standard_deduction_benefit - total_rent - (capital_gains_tax_owed if stocks_enabled else 0):,.0f}
• Net Income Advantage: {"HOME" if ((home_sale_gains + total_interest_tax_savings + capital_gains_tax_savings) - (total_interest + total_maintenance + total_property_tax + total_selling_costs)) > ((stock_investment_gains if stocks_enabled else 0) + rental_standard_deduction_benefit - total_rent - (capital_gains_tax_owed if stocks_enabled else 0)) else "RENTAL + INVESTMENT"}
• Net Income Difference: ${abs(((home_sale_gains + total_interest_tax_savings + capital_gains_tax_savings) - (total_interest + total_maintenance + total_property_tax + total_selling_costs)) - ((stock_investment_gains if stocks_enabled else 0) + rental_standard_deduction_benefit - total_rent - (capital_gains_tax_owed if stocks_enabled else 0))):,.0f}
        """
        
        summary_label = tk.Text(summary_frame, wrap=tk.NONE, font=('Courier', 10))
        summary_label.insert('1.0', summary_text)
        summary_label.config(state='disabled')
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(summary_frame, orient='vertical', command=summary_label.yview)
        h_scrollbar = ttk.Scrollbar(summary_frame, orient='horizontal', command=summary_label.xview)
        summary_label.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        summary_label.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=20, pady=20)
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=20)
        
        summary_frame.columnconfigure(0, weight=1)
        summary_frame.rowconfigure(0, weight=1)

def main():
    root = tk.Tk()
    app = HomeRentCalculator(root)
    root.mainloop()

if __name__ == "__main__":
    main() 