# financial_health.py
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.patches import Patch
from budgetManagement import IncomeTracker  # Import the IncomeTracker class
from emergencyFund import EmergencyFund
from debtManagement import DebtManagement

class FinancialHealth:
    def __init__(self, income_tracker):
        """
        Initializes the FinancialHealth with a given IncomeTracker instance.
        """
        self.income_tracker = income_tracker
        self.debt_manager = DebtManagement()  # Instantiate DebtManagement
        self.savings = 0
        self.liquid_assets = 0
        self.total_debts = 0
        self.bank_accounts = {}  # Store bank account balances
        self.historical_scores = []  # To store historical scores for plotting
        self.historical_savings = []  # Store historical savings for trend analysis
        self.historical_debts = []  # Store historical debt data for trend analysis
    
    def update_savings(self, amount):
        """Updates the user's total savings."""
        self.savings = amount
        self.historical_savings.append(amount)

    def update_liquid_assets(self, amount):
        """Updates the user's total liquid assets."""
        self.liquid_assets = amount

    def update_total_debts(self, amount):
        """Updates the user's total debt amount."""
        self.total_debts = amount
        self.historical_debts.append(amount)

    def get_monthly_income(self):
        """Fetch the total monthly income using the IncomeTracker instance."""
        daily_income_total = self.income_tracker.total_income  # Daily equivalent total income
        monthly_income = daily_income_total * 30  # Approximate monthly income based on 30 days.
        return monthly_income

    def get_monthly_expenses(self):
        """Fetch the total monthly expenses using the IncomeTracker instance."""
        daily_expenses_total = self.income_tracker.total_expenses  # Daily equivalent total expenses
        monthly_expenses = daily_expenses_total * 30  # Approximate monthly expenses based on 30 days.
        return max(monthly_expenses, 1)  # Default to 1 to avoid division by zero.

    def calculate_financial_health_score(self):
        """Calculates the user's financial health score."""
        monthly_expenses = self.get_monthly_expenses()
        score = (self.savings + self.liquid_assets - self.total_debts) / monthly_expenses
        self.historical_scores.append(score)
        return round(score, 2)

    def get_status_indicator(self, score):
        """Determines the financial status based on the score."""
        if score > 1.5:
            return "Strong"
        elif 1 <= score <= 1.5:
            return "Stable"
        else:
            return "At Risk"

    def display_financial_health_score(self):
        """Calculates and displays the financial health score and status."""
        score = self.calculate_financial_health_score()
        status = self.get_status_indicator(score)
        print(f"Financial Health Score: {score}")
        print(f"Status: {status}")

        if status == "Strong":
            print("Recommendation: Keep up the good work! Consider diversifying your investments.")
        elif status == "Stable":
            print("Recommendation: Focus on increasing savings or paying down debt to improve your financial health.")
        else:
            print("Recommendation: Consider reducing monthly expenses and increasing savings to get back on track.")

    def plot_score_evolution(self):
        """Displays a line graph of the evolution of the financial health score over time."""
        if len(self.historical_scores) < 2:
            print("Not enough data to display score evolution.")
            return

        # Create a DataFrame for plotting
        df = pd.DataFrame({'Score': self.historical_scores})
        df['Month'] = df.index + 1  # Assume each score represents a month.

        # Plot the evolution of the score
        plt.figure(figsize=(10, 6))
        plt.plot(df['Month'], df['Score'], marker='o', linestyle='-', color='blue', label='Financial Health Score')
        plt.axhline(y=1, color='orange', linestyle='--', label='Stable Threshold')
        plt.axhline(y=1.5, color='green', linestyle='--', label='Strong Threshold')
        plt.title('Financial Health Score Evolution Over Time', fontsize=14)
        plt.xlabel('Month')
        plt.ylabel('Score')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

    #--------------------------------------------- Section 1.2: Income and Expense Summary --------------------------------------------
    def display_income_expense_summary(self):
        """Displays a bar graph comparing income and expenses and provides status alerts."""
        monthly_income = self.get_monthly_income()
        monthly_expenses = self.get_monthly_expenses()

        # Create a bar chart for income vs expenses
        categories = ['Monthly Income', 'Monthly Expenses']
        amounts = [monthly_income, monthly_expenses]
        
        # Determine the status based on the comparison
        if monthly_income > monthly_expenses:
            status = "On Track"
            message = "You're on track with a positive cash flow."
            bar_colors = ['green', 'green']
        elif monthly_income == monthly_expenses:
            status = "Caution"
            message = "Your income matches your expenses, be mindful of unexpected expenses."
            bar_colors = ['yellow', 'yellow']
        else:
            status = "Overspending"
            message = "You're overspending. Consider cutting back on expenses."
            bar_colors = ['red', 'red']
        
        # Display the bar chart
        plt.bar(categories, amounts, color=bar_colors)
        plt.title('Monthly Income vs Expenses Comparison')
        plt.ylabel('Amount ($)')
        plt.tight_layout()
        plt.show()

        # Display status and recommendation
        print(f"Status: {status}")
        print(message)

        if status == "Overspending":
            print("Recommendation: Review your expenses and find areas to cut back.")
        elif status == "Caution":
            print("Recommendation: Consider building a buffer in your savings for unplanned costs.")
        elif status == "On Track":
            print("Recommendation: Great job! You might consider increasing your savings or investing surplus funds.")

    #--------------------------------------------- Section 1.3: Savings Capacity Gauge --------------------------------------------
    def display_savings_capacity_gauge(self):
        """Displays a gauge chart showing the percentage of income saved."""
        monthly_income = self.get_monthly_income()
        monthly_expenses = self.get_monthly_expenses()
        
        if monthly_income == 0:
            print("Monthly income is zero. Cannot calculate savings capacity.")
            return

        # Calculate the savings capacity
        savings_capacity = ((monthly_income - monthly_expenses) / monthly_income) * 100
        savings_capacity = max(0, savings_capacity)  # Ensure the savings capacity is not negative.
        
        # Display the calculated savings capacity
        print(f"Savings Capacity: {savings_capacity:.2f}% of your income is being saved.")

        # Create a gauge-like plot using a pie chart with a single segment
        plt.figure(figsize=(6, 6))
        plt.pie([savings_capacity, 100 - savings_capacity],
                labels=[f'{savings_capacity:.1f}% Saved', f'{100 - savings_capacity:.1f}% Spent'],
                startangle=90,
                colors=['#66b3ff', '#ff9999'],
                wedgeprops={'width': 0.3})
        
        plt.title('Savings Capacity Gauge', fontsize=14)
        plt.tight_layout()
        plt.show()

        # Display recommendations based on the savings capacity
        if savings_capacity < 10:
            print("Recommendation: Aim to increase your savings rate by reducing discretionary spending.")
        elif savings_capacity < 20:
            print("Recommendation: Consider reviewing your budget for more savings opportunities.")
        else:
            print("Recommendation: You're doing well with saving. Consider exploring investment options for better growth.")

    #--------------------------------------------- Section 1.4: Debt vs. Savings/Assets Balance --------------------------------------------
    def display_debt_vs_savings_balance(self):
        """Displays a bar graph comparing total debts against savings and liquid assets."""
        total_savings_and_assets = self.savings + self.liquid_assets
        total_debts = self.total_debts

        # Create a bar chart for savings and debts
        categories = ['Total Debts', 'Total Savings & Assets']
        amounts = [total_debts, total_savings_and_assets]
        
        # Display the bar chart
        bar_colors = ['red', 'green']
        plt.bar(categories, amounts, color=bar_colors)
        plt.title('Debt vs. Savings & Assets Balance')
        plt.ylabel('Amount ($)')
        plt.tight_layout()
        plt.show()

        # Provide recommendations based on the comparison
        print(f"Total Debts: ${total_debts}")
        print(f"Total Savings & Assets: ${total_savings_and_assets}")

        if total_debts > total_savings_and_assets:
            print("Recommendation: Focus on reducing debts, especially high-interest ones.")
        elif total_debts == total_savings_and_assets:
            print("Recommendation: Aim to increase your savings to ensure greater financial security.")
        else:
            print("Recommendation: Great job maintaining a positive balance. Consider further investments or building an emergency fund.")

    def plot_debt_savings_trend(self):
        """Plots the trend of savings and debt over time."""
        if len(self.historical_savings) < 2 or len(self.historical_debts) < 2:
            print("Not enough data to display trend evolution.")
            return

        # Create a DataFrame for plotting
        df = pd.DataFrame({
            'Savings': self.historical_savings,
            'Debts': self.historical_debts
        })
        df['Month'] = df.index + 1  # Assume each entry represents a month.

        # Plot the savings vs. debt trend over time
        plt.figure(figsize=(10, 6))
        plt.plot(df['Month'], df['Savings'], marker='o', linestyle='-', color='green', label='Savings')
        plt.plot(df['Month'], df['Debts'], marker='x', linestyle='-', color='red', label='Debts')
        plt.title('Savings and Debt Trend Over Time', fontsize=14)
        plt.xlabel('Month')
        plt.ylabel('Amount ($)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
    #--------------------------------------------- Section 1.5: Bank Account Tracker --------------------------------------------

    def add_bank_account(self, account_name, balance):
        """
        Adds or updates a bank account balance.
        :param account_name: The name of the bank account (e.g., "Checking", "Savings").
        :param balance: The balance of the bank account.
        """
        self.bank_accounts[account_name] = balance
        print(f"Updated {account_name} account with balance: ${balance}")

    def remove_bank_account(self, account_name):
        """
        Removes a bank account from the tracker.
        :param account_name: The name of the bank account to remove.
        """
        if account_name in self.bank_accounts:
            del self.bank_accounts[account_name]
            print(f"Removed {account_name} account.")
        else:
            print(f"Account {account_name} does not exist.")

    def get_total_liquid_assets(self):
        """Calculates the total liquid assets from bank accounts and other liquid assets."""
        total_bank_balances = sum(self.bank_accounts.values())
        return total_bank_balances + self.liquid_assets

    def display_liquid_assets_pie_chart(self):
        """Displays a pie chart of the user's liquid assets across bank accounts and other assets."""
        if not self.bank_accounts and self.liquid_assets == 0:
            print("No bank accounts or liquid assets to display.")
            return

        # Prepare data for the pie chart
        data = self.bank_accounts.copy()
        if self.liquid_assets > 0:
            data["Other Liquid Assets"] = self.liquid_assets

        # Extract data for the pie chart
        labels = list(data.keys())
        sizes = list(data.values())
        colors = plt.cm.Paired(range(len(labels)))

        # Create the pie chart
        plt.figure(figsize=(8, 8))
        wedges, _, _ = plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        
        # Create custom legend patches to match the colors
        legend_patches = [Patch(color=colors[i], label=labels[i]) for i in range(len(labels))]
        
        # Add a legend with custom colored patches
        plt.legend(handles=legend_patches, loc="center left", bbox_to_anchor=(1, 0.5), fontsize=12)
        
        # Add the title
        plt.title('Liquid Assets Distribution', fontsize=16)
        
        plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.
        
        # Show the pie chart
        plt.tight_layout()
        plt.show()

    def display_total_liquid_assets(self):
        """Displays the total value of liquid assets including all bank accounts."""
        total_liquid_assets = self.get_total_liquid_assets()
        print(f"Total Liquid Assets: ${total_liquid_assets}")
#---------------------------------------------------Example Usage---------------------------------------------------------------------------------------------------
# # Example: Using the IncomeTracker with FinancialHealth

# # Instantiate the IncomeTracker and add some data
# income_tracker = IncomeTracker()
# income_tracker.add_income_source("Salary", 3000, 'M')
# income_tracker.add_income_source("Freelance", 500, 'M')
# income_tracker.add_expense_source("Rent", 1500, 'M')
# income_tracker.add_expense_source("Food", 400, 'M')
# income_tracker.add_expense_source("Entertainment", 200, 'M')

# # Instantiate the FinancialHealth class with the income_tracker instance
# financial_health = FinancialHealth(income_tracker)

# #--------------------------------------------------- Usage 1.1---------------------------------------------------------------------------------------------------

# # Update financial data for each month
# financial_health.update_savings(10000)
# financial_health.update_liquid_assets(5000)
# financial_health.update_total_debts(3000)
# financial_health.display_financial_health_score()

# # Update data for the next month with a slight increase in savings and decrease in debts
# financial_health.update_savings(10500)  # Increased savings
# financial_health.update_total_debts(2800)  # Decreased debts
# financial_health.display_financial_health_score()

# # Update data for another month with increased expenses
# income_tracker.add_expense_source("Vacation", 500, 'M')  # Adding a new expense in IncomeTracker
# financial_health.display_financial_health_score()

# # Update data for month 4 with more liquid assets
# financial_health.update_liquid_assets(5500)
# financial_health.display_financial_health_score()

# # Update data for month 5 with decreased savings and increased debts
# financial_health.update_savings(10000)  # Savings back to original
# financial_health.update_total_debts(3500)  # Slight increase in debt
# financial_health.display_financial_health_score()

# # Update data for month 6 with a significant debt reduction
# financial_health.update_total_debts(2000)
# financial_health.display_financial_health_score()

# # Now plot the evolution of the financial health score over these months
# financial_health.plot_score_evolution()

# #--------------------------------------------------- Usage 1.2---------------------------------------------------------------------------------------------------

# # Update financial data for each month
# financial_health.update_savings(10000)
# financial_health.update_liquid_assets(5000)
# financial_health.update_total_debts(3000)
# financial_health.display_financial_health_score()

# # # Display income and expense summary for insights
# financial_health.display_income_expense_summary()

# #--------------------------------------------------- Usage 1.3---------------------------------------------------------------------------------------------------

# # # Update financial data for the month
# financial_health.update_savings(10000)
# financial_health.update_liquid_assets(5000)
# financial_health.update_total_debts(3000)
# financial_health.display_financial_health_score()

# # # Display savings capacity gauge for insights
# financial_health.display_savings_capacity_gauge()

# #--------------------------------------------------- Usage 1.4---------------------------------------------------------------------------------------------------

# # # Update financial data for the month
# financial_health.update_savings(10000)
# financial_health.update_liquid_assets(5000)
# financial_health.update_total_debts(3000)
# financial_health.display_financial_health_score()

# # Display debt vs. savings balance and trend over time
# financial_health.display_debt_vs_savings_balance()
# financial_health.plot_debt_savings_trend()

# #--------------------------------------------------- Usage 1.5---------------------------------------------------------------------------------------------------

# # Update savings and other liquid assets
# financial_health.update_savings(10000)
# financial_health.update_liquid_assets(2000)

# # Add bank accounts
# financial_health.add_bank_account("Checking", 5000)
# financial_health.add_bank_account("Savings", 8000)

# # Remove a bank account
# financial_health.remove_bank_account("Savings")

# # Display the total liquid assets including all bank accounts
# financial_health.display_total_liquid_assets()

# # Display the pie chart of liquid assets
# financial_health.display_liquid_assets_pie_chart()