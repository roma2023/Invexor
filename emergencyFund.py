import plotly.graph_objects as go
import numpy as np


class EmergencyFund():
    def __init__(self):
        self.emergency_fund_goal = 0
        self.emergency_fund_progress = 0 # i.e savings
        self.remaining = 0 
    
    def set_emergency_fund_goal(self, monthly_expenses : float, num_months : int):
        self.emergency_fund_goal = monthly_expenses * num_months
    
    def set_emergency_fund_progress(self, amount_saved : float):
        self.emergency_fund_progress = amount_saved
    
    def set_amount_remaining_to_save(self):
        self.remaining =  self.emergency_fund_goal - self.emergency_fund_progress

    def get_time_to_reach_goal(self, amount_saved_per_month : float):
        time_to_save = round(self.remaining / amount_saved_per_month, 1)
        return time_to_save
    
    def emergency_fund_progess_gauge(self):
        progress_perc = round((self.emergency_fund_progress / self.emergency_fund_goal) * 100, 1)
        self.create_gauge(progress_perc, 0, 100, title = 'Emergency Fund Progress')
    
    def emergency_savings_progress_bar(self):
        self.create_progress_bar(value = self.emergency_fund_progress, max_value = self.emergency_fund_goal, title = "Amount Saved vs Goal")
    
    def savings_linear_graph(self, amount_saved_per_month : float):
        self.create_linear_graph(rate = amount_saved_per_month, goal = self.emergency_fund_goal)


    ''' ====================================== GRAPHS ====================================== '''
    def create_gauge(self, value : int = 0, min_value : int = 0, max_value :int = 10 , title : str = ""):
        fig = go.Figure(go.Indicator(
            mode="number+gauge",
            value=value,
            number={
                'suffix': '%',
                'font': {'size': 80, 'color': '#333333', 'family': 'Helvetica, Arial, sans-serif'},
            },
            gauge={
                'shape': "angular",
                'axis': {
                    'range': [min_value, max_value],
                    'tickwidth': 2,
                    'tickcolor': "rgba(0,0,0,0.4)",
                    'tickvals': [0, 20, 40, 60, 80, 100],
                    'ticktext': ['0', '20', '40', '60', '80', '100'],
                },
                'bar': {
                    'color': "#3b8eea",
                    'thickness': 0.65  # Increased thickness for better visibility
                },
                'bgcolor': "#E5E5E5",
                'steps': [
                    {'range': [min_value, max_value], 'color': "#f5f5f5"},  # Lighter background
                ],
            },
            domain={'x': [0, 1], 'y': [0, 1]}
        ))

        # Update layout for a refined appearance
        fig.update_layout(
            title={
                'text': title,
                'y': 0.85,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 22, 'color': '#555555', 'family': 'Helvetica, Arial, sans-serif'}
            },
            font={'family': "Helvetica, Arial, sans-serif"},
            paper_bgcolor="white",
            plot_bgcolor="white",
            width=700,
            height=500,
            margin={'t': 100, 'b': 0, 'l': 0, 'r': 0}
        )

        fig.show()
        return 
    # ====================================================================================================
        
    def create_progress_bar(self, value: int, max_value: int = 100, title: str = 'Progress'):
        # Create a bar chart with a single bar representing the progress
        fig = go.Figure()

        # Add the actual progress bar in blue
        fig.add_trace(go.Bar(
            x=[value],
            y=[''],
            orientation='h',
            marker=dict(
                color="#3b8eea",  # Blue color for the progress
                line=dict(color='#3b8eea', width=0)
            ),
            width=0.5,
            text=f'{value}/{max_value}',
            textposition='inside',  # Show text inside the bar for clarity
            insidetextanchor='middle',
            textfont=dict(color='white', size = 14),  # Increase font size for better visibility
            showlegend=False
        ))

        # Add a layout for the chart
        fig.update_layout(
            title={
                'text': f'{title}: {value}/{max_value}',
                'x': 0.5,
                'y': 0.85,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': {'size': 22, 'family': 'Roboto, sans-serif'}
            },
            xaxis=dict(
                range=[0, max_value],  # Set the range from 0 to max_value
                showgrid=False,
                zeroline=False,
                showticklabels=False,  # Hide tick labels for a cleaner look
                visible=False  # Hide axis lines and labels
            ),
            yaxis=dict(
                showticklabels=False,
                visible=False
            ),
            plot_bgcolor='#f5f5f5',
            paper_bgcolor='white',
            height=150,  # Increase height for a thicker bar
            margin=dict(t=60, b=20, l=20, r=20)
        )

        fig.show()
        return 

    # ==================================================================================================== #
    def create_linear_graph(self, rate : float, goal : float):
        # Calculate time to save in months
        time_to_save = goal / rate
        
        # Create an array of months (e.g., 0 to time_to_save)
        months = np.arange(0, time_to_save + 1)
        cumulative_savings = rate * months

        # Create a line graph with plotly
        fig = go.Figure(go.Scatter(
            x=months,
            y=cumulative_savings,
            mode='lines',
            line=dict(color='#3b8eea', width=4),
            name='Cumulative Savings'
        ))

        # Add a line for the goal amount for visual reference
        fig.add_hline(y=goal, line=dict(color='red', dash='dash'), annotation_text='Goal Amount', annotation_position='top right')

        # Update layout for better presentation
        fig.update_layout(
            title='Projection: Time to Reach Emergency Savings Goal',
            xaxis_title='Months',
            yaxis_title='Cumulative Savings ($)',
            font=dict(family='Roboto, sans-serif', size=14, color='#333333'),
            plot_bgcolor='white',
            paper_bgcolor='white',
            width=800,
            height=500,
            margin=dict(t=80, b=60, l=60, r=40),
            xaxis=dict(
                showgrid=True,
                gridcolor='lightgray',
                range=[0, time_to_save],
                linecolor='black',
                linewidth=2,
                showline=True,
                tickmode='linear',
                tick0=0,
                dtick=5,
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='lightgray',
                range=[0, goal],
                linecolor='black',
                linewidth=2,
                showline=True,
                tickmode='linear',
                tick0=0,
                dtick=1000,
                showticklabels=True,  # Show tick labels for the y-axis
            )
        )

        # Adjust the zero label visibility
        fig.update_xaxes(ticks="outside", tickangle=0, tickfont=dict(size=12))
        fig.update_yaxes(ticks="outside", tickfont=dict(size=12))

        fig.show()
        return

