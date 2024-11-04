# income_tracker.py
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import utilities


class IncomeTracker:
    def __init__(self):
        self.utilities = utilities.Utilities()
        self.income_sources = {}  # {source: (amount, frequency, daily_amount)}
        self.expenses_sources = {}  # {source: (amount, frequency, daily_amount)}
        self.total_income = 0
        self.total_expenses = 0

    def add_income_source(self, source, amount, frequency):
        """Add an income source with the specified frequency."""
        daily_amount = self.utilities.calculate_daily_amount(amount, frequency)
        self.income_sources[source] = (amount, frequency, daily_amount)
        self.total_income += daily_amount

    def add_expense_source(self, source, amount, frequency):
        """Add an expense source with the specified frequency."""
        daily_amount = self.utilities.calculate_daily_amount(amount, frequency)
        self.expenses_sources[source] = (amount, frequency, daily_amount)
        self.total_expenses += daily_amount

    def get_total_income(self):
        """Returns the total daily equivalent income."""
        return self.total_income

    def get_total_expenses(self):
        """Returns the total daily equivalent expenses."""
        return self.total_expenses

    def pie_chart_distribution(self, is_income=True):
        """Generates a pie chart for income or expenses distribution."""
        if is_income:
            total = self.total_income
            title = "Monthly Income Distribution"
            hash_map = self.income_sources
        else:
            total = self.total_expenses
            title = "Monthly Expenses Distribution"
            hash_map = self.expenses_sources

        if total == 0:
            print(f"No data to display for {title.lower()}.")
            return

        # Convert hash_map to a list for indexing
        hash_items = list(hash_map.items())

        # Define colors for the pie chart slices
        colors = plt.cm.Paired(range(len(hash_items)))

        # Calculate the percentage of each source along with its assigned color
        percentages = {
            key: (value[0] / total * 100, colors[i])
            for i, (key, value) in enumerate(hash_items)
        }

        # Filter out zero percentages for the pie chart
        filtered_percentages = {
            key: (value, color)
            for key, (value, color) in percentages.items()
            if value > 0
        }

        # Extract filtered values and colors for the pie chart
        pie_values = [value for value, color in filtered_percentages.values()]
        pie_colors = [color for value, color in filtered_percentages.values()]

        # Create the pie chart with non-zero values
        wedges, _, _ = plt.pie(pie_values, autopct="%1.1f%%", colors=pie_colors)

        # Create custom legend patches to match the colors
        legend_patches = [
            Patch(color=percentages[key][1], label=key) for key in percentages.keys()
        ]

        # Add a legend with custom colored patches
        plt.legend(
            handles=legend_patches,
            loc="center left",
            bbox_to_anchor=(0.9, 0.5),
            fontsize=12,
        )

        # Enlarge the title of the chart
        plt.title(title, fontsize=18)

        plt.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle

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

#---------------------------------------------------Example Usage---------------------------------------------------------------------------------------------------
incomeTrack = IncomeTracker()

# We can take user input for income and expenses or use sample data

# salary = int(input("Enter your salary: "))
# salary_frequency = input("Enter your salary frequency (input D for daily, W for weekly, M for monthly, or O for one-time): ")
# passive_income = int(input("Enter your passive income: "))
# passive_income_frequency = input("Enter your passive income frequency (input D for daily, W for weekly, M for monthly, or O for one-time): ")
# extra_income = int(input("Enter your extra income: "))
# extra_income_frequency = input("Enter your extra income frequency (input D for daily, W for weekly, M for monthly, or O for one-time): ")

# sample data
salary = 1000
salary_frequency = 'M'
passive_income = 500
passive_income_frequency = 'M'
extra_income = 200
extra_income_frequency = 'M'

# Adding income sources
incomeTrack.add_income_source("Salary", salary, salary_frequency)
incomeTrack.add_income_source("Passive Income", passive_income, passive_income_frequency)
incomeTrack.add_income_source("Extra Income", extra_income, extra_income_frequency)

# Adding example expenses
incomeTrack.add_expense_source("Rent", 1500, 'M')
incomeTrack.add_expense_source("Food", 500, 'M')
incomeTrack.add_expense_source("Entertainment", 200, 'M')

# Generate Pie Chart for Income Distribution
incomeTrack.pie_chart_distribution(is_income=True) 
incomeTrack.pie_chart_distribution(is_income=False) # expenses

# Generate Bar Graph for Total Income vs Total Expense
incomeTrack.bar_graph_income_vs_expenses1()
incomeTrack.bar_graph_income_vs_expenses2()