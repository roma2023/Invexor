import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import utilities
import datetime
from matplotlib.patches import Patch

class IncomeTracker:
    def __init__(self):
        self.utilities = utilities.Utilities()
        
        # {Salary: (1000, O, dailySalary), Investment: (500, D, dailyInvestment), Rental Income: (200, M, DailyRentalIncome)}
        self.income_sources = {}
        self.expenses_sources = {}
        self.budgets = {}  # New dictionary to store budgets for each expense category
        
        self.historical_income = []  # Stores historical income data
        self.historical_expenses = []  # Stores historical expense data
        
        self.savings_contributions = 0
        self.total_income = 0
        self.total_expenses = 0
#-------------------------------------------------------Income Tracking--------------------------------------------------------------------------------------------       
    def add_income_source(self, source, amount, frequency):
        daily_amount = self.utilities.calculate_daily_amount(amount, frequency)
        self.income_sources[source] = (amount, frequency, daily_amount)
        self.total_income += daily_amount
        
    def add_expense_source(self, source, amount, frequency):
        daily_amount = self.utilities.calculate_daily_amount(amount, frequency)
        self.expenses_sources[source] = (amount, frequency, daily_amount) 
        self.total_expenses += daily_amount
        
    def pie_chart_distribution(self, isIncome: bool):
        # Calculate the total income or expenses
        if isIncome:
            total = self.total_income
            title = "Monthly Income Distribution"
            hashMap = self.income_sources
        else:
            total = self.total_expenses 
            title = "Monthly Expenses Distribution"
            hashMap = self.expenses_sources
        
        hash_items = list(hashMap.items())  # Convert to a list for indexing
        
        # Define colors for the pie chart slices
        colors = plt.cm.Paired(range(len(hash_items)))  # Automatically generate distinct colors
        
        # Calculate the percentage of each source along with its assigned color
        percentages = {key: (value[0] / total * 100, colors[i]) for i, (key, value) in enumerate(hash_items)}
        
        # Filter out zero percentages for the pie chart
        filtered_percentages = {key: (value, color) for key, (value, color) in percentages.items() if value > 0}
        
        # Extract filtered values and colors for the pie chart
        pie_values = [value for value, color in filtered_percentages.values()]
        pie_colors = [color for value, color in filtered_percentages.values()]
        
        # Create the pie chart with non-zero values
        wedges, _, _ = plt.pie(pie_values, autopct='%1.1f%%', colors=pie_colors)
        
        # Create custom legend patches to match the colors
        legend_patches = [Patch(color=percentages[key][1], label=key) for key in percentages.keys()]
        
        # Add a legend with custom colored patches
        plt.legend(handles=legend_patches, loc="center left", bbox_to_anchor=(0.9, 0.5), fontsize=12)
        
        # Enlarge the title of the chart
        plt.title(title, fontsize=18)
        
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        
        # Show the pie chart
        plt.show()

    def bar_graph_income_vs_expenses1(self):
        # Get income and expense sources separately
        income_sources = {key: value[2] for key, value in self.income_sources.items()}
        expense_sources = {key: value[2] for key, value in self.expenses_sources.items()}

        # Sort income sources in descending order
        sorted_income = sorted(income_sources.items(), key=lambda x: x[1], reverse=True)
        
        # Sort expense sources in descending order
        sorted_expenses = sorted(expense_sources.items(), key=lambda x: x[1])
        
        # Combine sorted income and expenses
        all_sorted_categories = [item[0] for item in sorted_income] + [item[0] for item in sorted_expenses]
        
        # Create a DataFrame for the bar graph, ensuring alignment of categories
        data = {
            'Income': [income_sources.get(category, 0) for category in all_sorted_categories],
            'Expenses': [-expense_sources.get(category, 0) for category in all_sorted_categories]  # Negative for expenses
        }
        
        # Create a DataFrame with the correct order
        df = pd.DataFrame(data, index=all_sorted_categories)

        # Plot the bar graph
        ax = df.plot(kind='bar', stacked=True, figsize=(10, 6), color=['green', 'red'])

        # Add legends for income and expenses
        income_legend = [Patch(color='green', label=key) for key, _ in sorted_income]
        expense_legend = [Patch(color='red', label=key) for key, _ in sorted_expenses]

        # Add separate legend boxes
        income_legend_box = plt.legend(handles=income_legend, loc="upper left", title="Income", bbox_to_anchor=(0.75, 1), fontsize=10)
        plt.gca().add_artist(income_legend_box)  # To keep both legends
        plt.legend(handles=expense_legend, loc="upper right", title="Expenses", bbox_to_anchor=(0.25, 0.5), fontsize=10)

        # Add labels and title
        plt.xlabel('Categories')
        plt.ylabel('Amount (Daily Equivalent)')
        plt.title('Segmented Income vs Expenses')

        # Display the bar graph
        plt.show()

    def bar_graph_income_vs_expenses2(self):
        # Get income and expense sources separately
        income_sources = {key: value[2] for key, value in self.income_sources.items()}
        expense_sources = {key: value[2] for key, value in self.expenses_sources.items()}

        # Sort income sources in descending order
        sorted_income = sorted(income_sources.items(), key=lambda x: x[1], reverse=True)
        
        # Sort expense sources in descending order
        sorted_expenses = sorted(expense_sources.items(), key=lambda x: x[1])

        # Separate income and expense category names and values
        income_categories, income_values = zip(*sorted_income)
        expense_categories, expense_values = zip(*sorted_expenses)

        # Define some custom colors for the stacked bars
        income_colors = ['#ff9999','#66b3ff','#99ff99', '#ffcc99']
        expense_colors = ['#c2c2f0','#ffb3e6','#c4e17f', '#ff9999']

        # Create figure and axis
        fig, ax = plt.subplots()

        # Plot the stacked bar for income categories
        income_bottom = 0
        for i, value in enumerate(income_values):
            ax.bar('Income', value, bottom=income_bottom, label=income_categories[i], color=income_colors[i % len(income_colors)])
            income_bottom += value

        # Plot the stacked bar for expense categories
        expense_bottom = 0
        for i, value in enumerate(expense_values):
            ax.bar('Expenses', value, bottom=expense_bottom, label=expense_categories[i], color=expense_colors[i % len(expense_colors)])
            expense_bottom += value

        # Adding the title and labels
        ax.set_title('Income and Expenses Breakdown')
        ax.set_ylabel('Amount (Daily Equivalent)')

        # Display legend
        ax.legend(loc='upper right', bbox_to_anchor=(1.15, 1))

        # Show the plot
        plt.tight_layout()
        plt.show()
#-------------------------------------------------Budget Setting & Comparison---------------------------------------------------------------------------------------

    def set_budget(self, category, amount):
        """Set a budget for a specific expense category."""
        self.budgets[category] = amount    

    def budget_progress_bar(self):
        """Displays the budget utilization for each category."""
        budget_data = []
        
        # Iterate through the expense sources and compare with the budget
        for category, (amount, frequency, daily_amount) in self.expenses_sources.items():
            if category in self.budgets:
                budget = self.budgets[category]
                utilized = (amount / budget) * 100  # Calculate utilization percentage
                
                # If budget is exceeded, cap it at 100%
                utilized = min(utilized, 100)
                
                budget_data.append((category, utilized, budget))
                
        # Display progress bars for each category
        for category, utilized, budget in budget_data:
            print(f"Category: {category}, Utilized: {utilized:.2f}%, Budget: {budget}")
        
        # Visual progress bar using matplotlib
        categories = [item[0] for item in budget_data]
        utilization = [item[1] for item in budget_data]
        
        plt.bar(categories, utilization, color='blue')
        plt.axhline(y=100, color='r', linestyle='--')  # Reference line at 100%
        plt.ylabel('Budget Utilization (%)')
        plt.title('Budget Utilization by Category')
        plt.show()

    def check_budget_alerts(self):
        """Check for budget alerts: approaching or exceeding the budget."""
        alerts = []
        for category, (amount, _, _) in self.expenses_sources.items():
            if category in self.budgets:
                budget = self.budgets[category]
                utilization = (amount / budget) * 100
                
                if utilization > 100:
                    alerts.append(f"Exceeded budget for {category}! Spending is at {utilization:.2f}% of the budget.")
                elif utilization >= 80:
                    alerts.append(f"Approaching budget limit for {category}. Spending is at {utilization:.2f}% of the budget.")
        
        # Display all alerts
        for alert in alerts:
            print(alert)
         
#-------------------------------------------------Real-Time Budget Comparison----------------------------------------------------------------------------------------
        
    def real_time_budget_comparison(self):
        """Display a real-time comparison of total income vs total expenses."""
        total_income = sum([income[2] for income in self.income_sources.values()])
        total_expenses = sum([expense[2] for expense in self.expenses_sources.values()])
        
        # Create a bar chart for income vs expenses
        categories = ['Total Income', 'Total Expenses']
        amounts = [total_income, total_expenses]
        
        # Color coding for surplus/deficit indication
        if total_income > total_expenses:
            bar_colors = ['green','green']
        elif total_income == total_expenses:
            bar_colors = ['yellow','yellow']
        else:
            bar_colors = ['red','red']
        
        plt.bar(categories, amounts, color=bar_colors)
        plt.title('Real-Time Budget Comparison')
        plt.ylabel('Amount (Daily Equivalent)')
        
        # Determine surplus/deficit message
        if total_income > total_expenses:
            suggestion = f"Surplus: You have a positive cash flow of ${total_income - total_expenses:.2f} per day."
        elif total_income == total_expenses:
            suggestion = "Break-even: Your income matches your expenses."
        else:
            suggestion = f"Deficit: You are overspending by ${total_expenses - total_income:.2f} per day."
        
        # Suggest adjustments if in deficit
        adjustment = self.suggest_adjustments(total_income, total_expenses)
        
        msg =  f"{suggestion}\n{adjustment}"
        
        print(msg)
        
        # Adjust plot layout to make space for the suggestion text
        plt.subplots_adjust(bottom=0.2)
        
        # Show the plot
        plt.show()
             
    def suggest_adjustments(self, total_income, total_expenses):
        """Provide suggestions to avoid or reduce a deficit."""
        if total_expenses > total_income:
            # Find the largest expense categories for adjustment suggestions
            largest_expense = max(self.expenses_sources.items(), key=lambda x: x[1][2])
            category, (amount, frequency, daily_amount) = largest_expense
            adjustment =  f"Suggestion: Consider reducing your spending in {category}, which accounts for ${daily_amount:.2f} daily."
            
        elif total_income > total_expenses:
            adjustment = "You have surplus funds. Consider investing or saving."
            
        else:
            adjustment = "Your income matches your expenses exactly. Consider reviewing your budget to see if you can save or invest some funds for future needs."

        return adjustment

#---------------------------------------------Disposable Income & Money Left to Invest--------------------------------------------------------------------------------

    def add_savings_contributions(self, amount):
        """Add a user-defined amount for savings."""
        self.savings_contributions = amount

    def calculate_disposable_income(self):
        """Calculate disposable income (income minus essential expenses)."""
        essential_expenses = ['Rent', 'Utilities', 'Debt Payments', 'Groceries', 'Transportation']
        
        total_essential_expenses = sum(
            value[2] for key, value in self.expenses_sources.items() if key in essential_expenses
        )
        total_income = sum([income[2] for income in self.income_sources.values()])
        
        disposable_income = total_income - total_essential_expenses
        return max(0, disposable_income)  # Ensure disposable income cannot be negative
    
    def calculate_money_left_to_invest(self, disposable_income):
        """Calculate how much money is left to invest after savings contributions."""
        # If savings contributions exceed disposable income, we reduce the savings contributions
        savings_contributions = min(self.savings_contributions, disposable_income)
        return max(0, disposable_income - savings_contributions)

    def disposable_income_summary(self):
        """Display a summary of disposable income, savings, and investment options."""
        disposable_income = self.calculate_disposable_income()
        money_left_to_invest = self.calculate_money_left_to_invest(disposable_income)
        
        # Adjust savings contributions if they exceed the disposable income
        actual_savings_contributions = min(self.savings_contributions, disposable_income)
        

        
        # Data preparation for the pie chart (filter out zero values)
        allocations = {'Savings Contributions': actual_savings_contributions, 
                       'Money Left to Invest': money_left_to_invest}
        filtered_allocations = {key: value for key, value in allocations.items() if value > 0}
        
        # Define colors and labels
        labels = list(filtered_allocations.keys())
        sizes = list(filtered_allocations.values())
        colors = plt.cm.Paired(range(len(labels)))  # Automatically generate distinct colors
        
        # Create the pie chart
        wedges, _, _ = plt.pie(sizes, autopct='%1.1f%%', colors=colors)
        
        # Create custom legend patches to match the colors
        legend_patches = [Patch(color=colors[i], label=label) for i, label in enumerate(labels)]
        
        # Add a legend with custom colored patches
        plt.legend(handles=legend_patches, loc="center left", bbox_to_anchor=(0.9, 0.5), fontsize=12)
        
        # Add the title
        plt.title('Disposable Income Allocation', fontsize=18)
        
        plt.axis('equal')  # Ensure pie chart is circular
        
        # Print a summary
        summary1 = f"Total Disposable Income: ${disposable_income:.2f}"
        summary2 = f"Savings Contributions: ${actual_savings_contributions:.2f}"
        summary3 = f"Money Left to Invest: ${money_left_to_invest:.2f}"
        
        msg =  f"{summary1}\n{summary2}\n{summary3}"
        
        # Display the suggestion text below the graph using plt.text()
        plt.text(0, -1.3, msg, fontsize=12, color="black", ha='center', wrap=True)
        # Show the pie chart
        plt.show()

        # Provide investment suggestions
        if money_left_to_invest > 0:
            print(f"Suggestion: You can consider investing ${money_left_to_invest:.2f} into stocks, mutual funds, or other investments based on your financial goals.")
        else:
            print("Suggestion: Focus on building more savings before considering investments.")

#------------------------------------------------Forecasted Budget & Income Projection------------------------------------------------------------------------------

    def add_historical_data(self, income, expenses):
        """Add historical income and expense data (e.g., from previous months)."""
        self.historical_income.append(income)
        self.historical_expenses.append(expenses)
    
    def forecast_income_expenses(self, months=6):
        """Forecast future income and expenses based on historical data."""
        # Use average of historical income and expenses for forecasting
        avg_income = np.mean(self.historical_income)
        avg_expenses = np.mean(self.historical_expenses)
        
        # Forecast income and expenses for each of the next 'months'
        projected_income = [avg_income] * months
        projected_expenses = [avg_expenses] * months
        
        return projected_income, projected_expenses

    def forecast_disposable_income(self, months=6):
        """Forecast disposable income for the next X months."""
        projected_income, projected_expenses = self.forecast_income_expenses(months)
        
        # Calculate projected disposable income (income - expenses)
        projected_disposable_income = [income - expense for income, expense in zip(projected_income, projected_expenses)]
        
        return projected_disposable_income

    def forecast_with_planned_expenses(self, months=6, planned_expenses=None):
        """Include planned expenses into the forecast."""
        projected_income, projected_expenses = self.forecast_income_expenses(months)
        
        # Initialize planned expenses if none provided
        if planned_expenses is None:
            planned_expenses = np.zeros(months)  # No planned expenses initially
        
        # Ensure planned_expenses has the right length
        if len(planned_expenses) != months:
            raise ValueError(f"Planned expenses must be a list with {months} values.")
        
        # Adjust projected expenses to include planned discretionary expenses
        adjusted_expenses = [proj_exp + plan_exp for proj_exp, plan_exp in zip(projected_expenses, planned_expenses)]
        
        # Calculate disposable income with adjusted expenses
        projected_disposable_income = [income - expense for income, expense in zip(projected_income, adjusted_expenses)]
        
        return projected_disposable_income, adjusted_expenses
    
    def plot_forecast(self, months=6, planned_expenses=None):
        """Plot income, expenses, and disposable income forecast."""
        projected_income, adjusted_expenses = self.forecast_income_expenses(months)
        projected_disposable_income, _ = self.forecast_with_planned_expenses(months, planned_expenses)
        
        months_list = list(range(1, months + 1))
        
        # Plot forecast data
        plt.figure(figsize=(10, 6))
        
        plt.plot(months_list, projected_income, label="Projected Income", color="green", marker='o')
        plt.plot(months_list, adjusted_expenses, label="Projected Expenses", color="red", marker='x')
        plt.plot(months_list, projected_disposable_income, label="Projected Disposable Income", color="blue", marker='s')
        
        plt.xlabel("Months")
        plt.ylabel("Amount ($)")
        plt.title(f"Forecast for Next {months} Months")
        plt.legend()
        plt.grid(True)
        
        # Show the plot
        plt.tight_layout()
        plt.show()

    def forecast_alerts(self, months=6, planned_expenses=None):
        """Check if any future months show a deficit and provide adjustment suggestions."""
        projected_disposable_income, _ = self.forecast_with_planned_expenses(months, planned_expenses)
        
        for month, disposable_income in enumerate(projected_disposable_income, 1):
            if disposable_income < 0:
                print(f"Alert: You are projected to face a deficit of ${-disposable_income:.2f} in month {month}. Consider adjusting your spending or increasing income.")

# #---------------------------------------------------Example Usage---------------------------------------------------------------------------------------------------
# incomeTrack = IncomeTracker()

# # We can take user input for income and expenses or use sample data

# # # salary = int(input("Enter your salary: "))
# # # salary_frequency = input("Enter your salary frequency (input D for daily, W for weekly, M for monthly, or O for one-time): ")
# # # passive_income = int(input("Enter your passive income: "))
# # # passive_income_frequency = input("Enter your passive income frequency (input D for daily, W for weekly, M for monthly, or O for one-time): ")
# # # extra_income = int(input("Enter your extra income: "))
# # # extra_income_frequency = input("Enter your extra income frequency (input D for daily, W for weekly, M for monthly, or O for one-time): ")

# # sample data
# salary = 1000
# salary_frequency = 'M'
# passive_income = 500
# passive_income_frequency = 'M'
# extra_income = 200
# extra_income_frequency = 'M'

# # Adding income sources
# incomeTrack.add_income_source("Salary", salary, salary_frequency)
# incomeTrack.add_income_source("Passive Income", passive_income, passive_income_frequency)
# incomeTrack.add_income_source("Extra Income", extra_income, extra_income_frequency)

# # Adding example expenses
# incomeTrack.add_expense_source("Rent", 1500, 'M')
# incomeTrack.add_expense_source("Food", 500, 'M')
# incomeTrack.add_expense_source("Entertainment", 200, 'M')

# # #----------------------------------------------------------2.1---------------------------------------------------------------------
# # # Generate Pie Chart for Income Distribution
# # incomeTrack.pie_chart_distribution(isIncome=True)
# # incomeTrack.pie_chart_distribution(isIncome=False)

# # # Generate Bar Graph for Total Income vs Total Expense
# # incomeTrack.bar_graph_income_vs_expenses1()
# # incomeTrack.bar_graph_income_vs_expenses2()

# # #----------------------------------------------------------2.2---------------------------------------------------------------------
# # Setting budgets
# incomeTrack.set_budget("Rent", 1500)
# incomeTrack.set_budget("Food", 600)
# incomeTrack.set_budget("Entertainment", 300)

# # Checking budget utilization
# incomeTrack.budget_progress_bar()

# # Checking for alerts
# incomeTrack.check_budget_alerts()

# # #-----------------------------------------------------------2.3-------------------------------------------------------------------
# # Real-time budget comparison
# incomeTrack.real_time_budget_comparison()

# # #-----------------------------------------------------------2.4-------------------------------------------------------------------
# # Add savings contributions
# incomeTrack.add_savings_contributions(300)

# # Display disposable income and investment summary
# incomeTrack.disposable_income_summary()

# # #-----------------------------------------------------------2.5-------------------------------------------------------------------
# # Adding historical data (e.g., income and expenses for the last 3 months)
# incomeTrack.add_historical_data(3000, 2500)
# incomeTrack.add_historical_data(3100, 2600)
# incomeTrack.add_historical_data(3200, 2700)

# # Simulating planned expenses over the next 6 months
# planned_expenses = [0, 0, 1000, 0, 500, 0]  # Example: Vacation in month 3 and a large purchase in month 5

# # Plotting income, expenses, and disposable income forecast for the next 6 months with planned expenses
# incomeTrack.plot_forecast(months=6, planned_expenses=planned_expenses)

# # Checking for alerts (deficits) in the future
# incomeTrack.forecast_alerts(months=6, planned_expenses=planned_expenses)