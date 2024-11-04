import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class DebtManagement:
    def __init__(self):
        self.debts = {}  # Store debts with their balance, interest rate, and urgency (optional)
        self.debt_history = {}  # Store history of debt payments

#-------------------------------------------------------Debt Prioritization--------------------------------------------------------------------------------------------       

    def add_debt(self, name, balance, interest_rate, urgency=1):
        """
        Adds a debt with balance, interest rate, and urgency.
        Urgency is optional and defaults to 1.
        """
        self.debts[name] = {
            'balance': balance,
            'interest_rate': interest_rate,
            'urgency': urgency
        }
        self.debt_history[name] = [balance]  # Initialize history with the initial balance

    def prioritize_debts(self):
        """
        Prioritizes debts based on interest rate, balance, and urgency.
        Returns a sorted list of debts.
        """
        # Sort debts by interest rate (descending), then balance (ascending), then urgency (descending)
        sorted_debts = sorted(
            self.debts.items(),
            key=lambda x: (-x[1]['interest_rate'], x[1]['balance'], -x[1]['urgency'])
        )
        
        # Display prioritized debt list
        print("Prioritized Debt List:")
        for debt, details in sorted_debts:
            print(f"{debt}: Balance = ${details['balance']}, Interest Rate = {details['interest_rate']}%, Urgency = {details['urgency']}")
        
        return sorted_debts
    
#-------------------------------------------------------Debt Payment Progress--------------------------------------------------------------------------------------------       

    def make_payment(self, name, payment):
        """
        Makes a payment towards a specific debt, reducing its balance.
        """
        if name in self.debts:
            # Calculate new balance after payment
            new_balance = max(0, self.debts[name]['balance'] - payment)
            self.debts[name]['balance'] = new_balance
            # Record the new balance in the history
            self.debt_history[name].append(new_balance)
        else:
            print(f"Debt {name} not found.")
    
    def plot_debt_progress(self):
        """
        Plots a bar graph showing the remaining balance of each debt over time.
        """
        # Find the maximum length of the history lists
        max_length = max(len(history) for history in self.debt_history.values())
        
        # Pad all histories with NaN to match the maximum length
        padded_history = {name: history + [np.nan] * (max_length - len(history))
                          for name, history in self.debt_history.items()}

        # Prepare data for plotting
        df = pd.DataFrame(padded_history)

        # Plot the bar graph with historical data for each debt
        df.plot(kind='bar', stacked=True, figsize=(10, 6))
        
        plt.title("Debt Payment Progress Over Time")
        plt.xlabel("Payment Instances")
        plt.ylabel("Remaining Balance ($)")
        plt.legend(title="Debt Name")
        plt.grid(axis='y', linestyle='--', linewidth=0.7)
        
        # Show the plot
        plt.tight_layout()
        plt.show()

    def plot_debt_progress_line(self):
        """
        Plots a line chart showing the remaining balance of each debt over time.
        """
        # Find the maximum length of the history lists
        max_length = max(len(history) for history in self.debt_history.values())
        
        # Pad all histories with NaN to match the maximum length
        padded_history = {name: history + [np.nan] * (max_length - len(history))
                        for name, history in self.debt_history.items()}

        # Prepare data for plotting
        df = pd.DataFrame(padded_history)

        # Plot the line chart
        df.plot(kind='line', marker='o', figsize=(10, 6))
        
        plt.title("Debt Payment Progress Over Time")
        plt.xlabel("Payment Instances")
        plt.ylabel("Remaining Balance ($)")
        plt.legend(title="Debt Name")
        plt.grid(axis='y', linestyle='--', linewidth=0.7)
        
        # Show the plot
        plt.tight_layout()
        plt.show()

#-------------------------------------------------------Extra Payment Suggestions--------------------------------------------------------------------------------------------       

    def suggest_extra_payments(self, disposable_income, percentage=0.2):
        """
        Suggest extra payments based on disposable income.
        """
        # Calculate the suggested extra payment amount as a percentage of disposable income
        extra_payment = disposable_income * percentage

        # Sort debts by interest rate in descending order (focus on highest-interest debts first)
        sorted_debts = sorted(
            self.debts.items(),
            key=lambda x: -x[1]['interest_rate']
        )
        
        suggestions = []
        
        for name, details in sorted_debts:
            balance = details['balance']
            interest_rate = details['interest_rate']
            
            if balance > 0:
                # Calculate interest savings if the extra payment is applied to this debt
                monthly_interest_rate = interest_rate / 12 / 100
                interest_savings = extra_payment * monthly_interest_rate
                
                suggestion = (
                    f"Extra payment of ${extra_payment:.2f} towards {name} "
                    f"could save you around ${interest_savings:.2f} in interest this month."
                )
                suggestions.append(suggestion)
        
        # Display suggestions
        if suggestions:
            print("Extra Payment Suggestions:")
            for suggestion in suggestions:
                print(suggestion)
        else:
            print("No active debts to suggest extra payments for.")

#-------------------------------------------------------Debt Payoff Calculator--------------------------------------------------------------------------------------------       

    def calculate_payoff_time(self, name, monthly_payment):
        """
        Calculates the estimated time to pay off a debt.
        """
        if name not in self.debts:
            print(f"Debt {name} not found.")
            return

        balance = self.debts[name]['balance']
        interest_rate = self.debts[name]['interest_rate'] / 100
        monthly_interest_rate = interest_rate / 12

        # Check if the monthly payment is sufficient to reduce the balance
        if monthly_payment <= balance * monthly_interest_rate:
            print(f"Monthly payment of ${monthly_payment:.2f} is too low to pay off {name}. Increase the payment amount.")
            return

        # Calculate the number of months to pay off the debt
        try:
            n = np.log(monthly_payment / (monthly_payment - balance * monthly_interest_rate)) / np.log(1 + monthly_interest_rate)
            n = np.ceil(n)  # Round up to the nearest whole month

            print(f"Payoff time for {name} with a monthly payment of ${monthly_payment:.2f} is approximately {int(n)} months.")
        except ValueError:
            print(f"Error calculating payoff time for {name}. Please check the input values.")

    def show_adjusted_payoff(self, name, monthly_payment, adjustment_percentages=[10, 20, 30]):
        """
        Shows how adjusting the payment amount affects the payoff timeline.
        """
        print(f"\nImpact of Payment Adjustments for {name}:")
        for percentage in adjustment_percentages:
            adjusted_payment = monthly_payment * (1 + percentage / 100)
            print(f"\nWith a {percentage}% increase:")
            self.calculate_payoff_time(name, adjusted_payment)

#---------------------------------------------------Example Usage---------------------------------------------------------------------------------------------------

# # Create an instance of the DebtManagement class
# debt_manager = DebtManagement()

# # Add debts
# debt_manager.add_debt("Credit Card A", 3000, 18.5, urgency=2)
# debt_manager.add_debt("Car Loan", 8000, 4.5, urgency=3)
# debt_manager.add_debt("Student Loan", 12000, 5.6)

# #----------------------------------------------------------4.1---------------------------------------------------------------------

# # Get the prioritized list of debts
# debt_manager.prioritize_debts()

# #----------------------------------------------------------4.2---------------------------------------------------------------------

# # Make some payments towards the debts
# debt_manager.make_payment("Credit Card A", 500)
# debt_manager.make_payment("Student Loan", 1000)
# debt_manager.make_payment("Car Loan", 600)
# debt_manager.make_payment("Credit Card A", 300)
# debt_manager.make_payment("Student Loan", 800)

# print(debt_manager.debt_history)

# # Plot the debt payment progress as a bar chart
# debt_manager.plot_debt_progress()

# # Plot the debt payment progress as a line chart
# debt_manager.plot_debt_progress_line()

# #----------------------------------------------------------4.3---------------------------------------------------------------------

# # Example disposable income
# disposable_income = 500

# # Suggest extra payments (e.g., 20% of disposable income)
# debt_manager.suggest_extra_payments(disposable_income, percentage=0.2)

# #----------------------------------------------------------4.4---------------------------------------------------------------------

# # Calculate payoff time for a debt with a given monthly payment
# debt_manager.calculate_payoff_time("Credit Card A", 200)  # Example: $200 monthly payment

# # Show how increasing the monthly payment by different percentages affects the payoff time
# debt_manager.show_adjusted_payoff("Credit Card A", 200, adjustment_percentages=[10, 20, 30])
