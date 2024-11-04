import matplotlib.pyplot as plt
import numpy as np

def yes_or_no_input(prompt):
    i = input(prompt)
    if (i != "yes") and (i != "no"):
        print("Invalid input. Please enter \'yes\' or \'no\'. \n")
        return yes_or_no_input(prompt)
    else:
        return i

def float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a valid float. \n")


def make_budget(timeframe : str = "monthly") -> dict: 
    # (1) Specify Net Income from User 
    net_income = float_input(f"What is your {timeframe} income? \n")

    # (2) Ask user to create a budget for general categories 
    budget : dict = {}
    general_categories = ["food and groceries", "rent", "entertainment", "transportation"]  

    for category in general_categories: 

        category_budget = float_input(f"What is your {timeframe} budget for {category}? \n") 
        if (net_income - category_budget < 0):
            print(f"Invalid budget, you have exceeded your {timeframe} income\n")
            return {}
        
        budget_spent = float_input(f"How much of your {timeframe} budget for {category} have you spent already? \n")        
        if (category_budget < budget_spent):
            print(f"Invalid budget, you have exceeded your budget already.\n")
            return {}

        else:
            net_income = net_income - category_budget
            budget[category] = (category_budget, budget_spent)
    
    # (3) Allow user to create budget for their personally defined categories
    flag = True 
    while (flag == True):
        make_new = yes_or_no_input("Would you like to add any other expense to your budget? (yes/no) \n")
        
        if make_new == "no":
            flag = False
        
        else: 
            new_category_name = input("What is the category of your expense?\n")

            category_budget = float_input(f"What is your {timeframe} budget for {new_category_name}?\n") 
            if (net_income - category_budget < 0):
                print(f"Invalid budget, you have exceeded your {timeframe} income\n")
                return {}

            budget_spent = float_input(f"How much of your {timeframe} budget for {new_category_name} have you spent already?\n")
            if (category_budget < budget_spent):
                        print(f"Invalid budget, you have exceeded your budget already.\n")
                        return {}
            
            else:
                budget[new_category_name] = (category_budget, budget_spent)

    # (4) Return budget 
    print("Budget has been created succesfully!\n")
    return budget


class BUDGET():
    def __init__(self, income : float, budget : dict):
        self.income = income 
        self.budget = budget

    ''' ======================== BUDGET MANIPULATION FUNCTIONS  ======================== '''
    def calculate_total_budget(self):
        total_budget = 0
        for key in self.budget:
            total_budget += self.budget[key][0]
        return total_budget

    def add_budget_category(self, category_name : str, budget_amount : float, amount_spent : float):
        if (self.income < (self.calculate_total_budget() + budget_amount)):
            return -1 # Error, category won't be added 
        else:
            self.budget[category_name] = (budget_amount, amount_spent)
            return 1
    
    def spend_money_from_budget(self, category_name : str, amount_spent : float):
        budget = self.budget[category_name][0]
        spent = self.budget[category_name][1]
        self.budget[category_name] = (budget, spent + amount_spent)
        return 
    
    def change_budget_amount(self, category_name : str, new_budget : float):
        spent = self.budget[category_name][1]
        self.budget[category_name] = (new_budget, spent)
        return 
    
    def get_on_and_off_budget_categories(self):
        green_categories = []
        red_categories = []
        for key in self.budget:
            budget = self.budget[key][0]
            spent = self.budget[key][1]
            if spent < budget: 
                green_categories.append(key)
            else:
                red_categories.append(key)

        return green_categories, red_categories

    def get_alert_categories(self, threshold : int = 80):
        green_categories = []
        red_categories = []
        for key in self.budget:
            budget = self.budget[key][0]
            spent = self.budget[key][1]
            if ((spent/budget) * 100) < threshold: 
                green_categories.append(key)
            else:
                red_categories.append(key)

        return green_categories, red_categories
    
    ''' ==================================== CHARTS ==================================== ''' 
    def budget_vs_income_pie(self):
        total_budget = self.calculate_total_budget()
        
        # (1) Calculate percentages
        budgeted_percentage = (total_budget / self.income) * 100
        remaining_percentage = 100 - budgeted_percentage

        # (2) Create pie chart
        labels = ['Budgeted', 'Remaining']
        sizes = [budgeted_percentage, remaining_percentage]
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['#66b3ff','#ff9999'])
        plt.axis('equal')  
        plt.legend(labels, title="Income Breakdown")
        plt.title(f"Budget Allocation")
        plt.show()
        return 

    '''
        'include_total' - if == True it will include a bar for the total budget vs spent
                          across all categories.
        'categories_to_include' - if empty, it will include all categories.
    '''
    def budget_vs_categories_and_spent(self, include_total: bool = True, categories_to_include: list = []):
        # If no specific categories are provided, use all categories
        if not categories_to_include:
            categories = list(self.budget.keys())
        else:
            categories = [category for category in categories_to_include if category in self.budget]  # Include only valid categories

        # Data for each category
        total_budget = sum([self.budget[category][0] for category in categories])  # Total budget across all categories
        total_spent = sum([self.budget[category][1] for category in categories])  # Total spent across all categories
        budgeted = [self.budget[category][0] for category in categories]  # Budget for each category
        spent = [self.budget[category][1] for category in categories]  # Amount spent for each category

        # Adjust figure size based on number of categories (with a minimum size)
        fig_height = max(2, len(categories) * 1.2)
        fig, ax = plt.subplots(figsize=(12, fig_height))  # Adjusted figure size dynamically

        # Add bars for each category
        y = np.arange(len(categories) + int(include_total))  # Add one more for the total if requested
        bars_budget = ax.barh(y[:len(categories)], budgeted, color='green', edgecolor='black', label='Budget')
        bars_spent = ax.barh(y[:len(categories)], spent, color='red', edgecolor='black', label='Spent')

        # Add total bar for total budget and total spent across all categories (IF REQUESTED)
        if include_total:
            ax.barh(y[-1], total_budget, color='green', edgecolor='black')
            ax.barh(y[-1], total_spent, color='red', edgecolor='black')

        # Add labels for each category, and append 'Total' if total is included
        labels = categories + (['Total'] if include_total else [])
        ax.set_yticks(y)
        ax.set_yticklabels(labels, fontsize=12, fontweight='normal')

        # Add grid lines
        ax.xaxis.grid(True, linestyle='--', alpha=0.5)
        ax.set_axisbelow(True)

        # Add title and labels
        ax.set_title("Budget vs Spent", fontsize=16, fontweight='light', pad=20)
        ax.set_xlabel("Amount", fontsize=14)

        # Adjusting the font for better visibility
        plt.rc('font', family='DejaVu Sans', weight='light')

        # Add a larger legend and move it outside the plot
        ax.legend(['Budget', 'Spent'], loc='upper right', fontsize=12, frameon=False, bbox_to_anchor=(1.15, 1))

        # Increase the layout padding to allow room for labels
        plt.tight_layout(pad=3)

        # Display the chart
        plt.show()
        return

    

    ''' ================================== =================================='''


            
def make_budget_progess_bar(net_income : float, budget_dict : dict):
    pass


#d = make_budget()
#print(d)

d = {'food and groceries': (10.0, 1.0), 'rent': (10.0, 1.0), 'entertainment': (100.0, 2.0), 'transportation': (50.0, 40.0), 'Porn': (100.0, 20.0)}
c = BUDGET(1000, d)
c.budget_vs_categories_and_spent(0, [])