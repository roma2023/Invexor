import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Utilities:
    def __init__(self):
        pass
    
    def calculate_total_income(self, income):
        return sum(income)
    
    def calculate_daily_amount(self, amount, frequency):
        if frequency == 'D':
            return amount
        elif frequency == 'W':
            return amount / 7
        elif frequency == 'M':
            return amount / 30
        elif frequency == 'Y':
            return amount / 365
        else:
            return 0
    
    def calculate_total_expenses(self, expenses):
        return sum(expenses)
    
    def calculate_savings(self, income, expenses):
        return income - expenses
    
    def calculate_financial_health_score(self, income, expenses):
        return (income - expenses) / income
    
    def calculate_savings_capacity(self, income, expenses):
        return (income - expenses) / income
    
    def calculate_debt_to_income_ratio(self, income, expenses):
        return expenses / income
    
    def calculate_net_worth(self, income, expenses):
        return income - expenses
    
    def calculate_monthly_cash_flow(self, income, expenses):
        return income - expenses
    
    def calculate_monthly_savings(self, income, expenses):
        return income - expenses
    
    def calculate_monthly_debt_payments(self, income, expenses):
        return expenses
    
    def calculate_monthly_discretionary_spending(self, income, expenses):
        return income - expenses
    
    def calculate_monthly_savings_rate(self, income, expenses):
        return (income - expenses) / income
    
    def pie_chart_expense_dsitribution(self, HashMap: dict): 
        plt.pie(HashMap.values(), labels=HashMap.keys(), autopct='%1.1f%%') 
        
        