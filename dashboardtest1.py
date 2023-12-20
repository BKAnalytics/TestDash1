#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install dash pandas openpyxl


# In[3]:


pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host=files.pythonhosted.org dash


# In[210]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import dcc, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random


# In[211]:


# Read initial data from CSV file
csv_file = 'fake.csv'
df = pd.read_csv(csv_file)


# In[212]:


# Define data types for columns
data_types = {'Country': 'object', 'Currency': 'float', 'Region': 'object', 'Full Name': 'object', 'Date': 'datetime64[ns]'}
df = df.astype(data_types)


# In[213]:


# Create a Dash web application
app = dash.Dash(__name__)


# In[214]:


# Define data types for columns
data_types = {'Country': 'object', 'Currency': 'float', 'Region': 'object', 'Full Name': 'object', 'Date': 'datetime64[ns]'}
df = df.astype(data_types)

# Create a Dash web application
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Test Dashboard"),

    # First Output - Scatter Plot
    html.Label("Select Value"),
    dcc.Dropdown(id='scatter-dropdown1', options=[
        {'label': 'Country', 'value': 'Country'},
        {'label': 'Region', 'value': 'Region'},
        {'label': 'Name', 'value': 'Full Name'}
    ], value='Country'),
    dcc.Dropdown(id='scatter-dropdown2', multi=True, value=[]),
    dcc.Graph(id='scatter-plot'),

    # Second Output - Pie Chart
    html.Label("Select Category for Pie Chart:"),
    dcc.Dropdown(id='pie-dropdown', options=[
        {'label': 'Country', 'value': 'Country'},
        {'label': 'Region', 'value': 'Region'},
    ], value='Country'),
    dcc.Dropdown(id='pie-dropdown2', multi=True, value=[]),
    dcc.Graph(id='pie-chart'),

    # Third Output - Line Chart
    html.Label("Select Date Range for Line Chart:"),
    dcc.DatePickerRange(id='date-picker-range',
                        start_date=df['Date'].min(),
                        end_date=df['Date'].max(),
                        display_format='YYYY-MM-DD'),
    dcc.Graph(id='line-chart'),

])

# Callbacks
# Callback for updating options of the second dropdown based on the selected value of the first dropdown
@app.callback(
    Output('scatter-dropdown2', 'options'),
    [Input('scatter-dropdown1', 'value')]
)
def update_second_dropdown(selected_dropdown1):
    if selected_dropdown1 == 'Country':
        options = [{'label': country, 'value': country} for country in df['Country'].unique()]
    elif selected_dropdown1 == 'Region':
        options = [{'label': region, 'value': region} for region in df['Region'].unique()]
    elif selected_dropdown1 == 'Full Name':
        options = [{'label': name, 'value': name} for name in df['Full Name'].unique()]
    else:
        options = []

    return options

# Callback for updating options of the second dropdown in the pie chart based on the selected value of the first dropdown
@app.callback(
    Output('pie-dropdown2', 'options'),
    [Input('pie-dropdown', 'value')]
)
def update_pie_dropdown(selected_dropdown):
    if selected_dropdown == 'Country':
        options = [{'label': country, 'value': country} for country in df['Country'].unique()]
    elif selected_dropdown == 'Region':
        options = [{'label': region, 'value': region} for region in df['Region'].unique()]
    else:
        options = []

    return options

# Callback for updating scatter plot based on selected values
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('scatter-dropdown1', 'value'),
     Input('scatter-dropdown2', 'value')]
)
def update_scatter_plot(selected_dropdown1, selected_dropdown2):
    # Example logic for updating the scatter plot based on selected values
    if not selected_dropdown2:
        selected_dropdown2 = df[selected_dropdown1].unique()

    filtered_df = df[df[selected_dropdown1].isin(selected_dropdown2)]
    scatter_plot_figure = px.scatter(filtered_df, x=selected_dropdown1, y='Currency', color='Country', size='Currency')
    return scatter_plot_figure

# Callback for updating pie chart based on selected values
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('pie-dropdown', 'value'),
     Input('pie-dropdown2', 'value')]
)
def update_pie_chart(selected_dropdown, selected_dropdown2):
    # Example logic for updating the pie chart based on selected values
    if not selected_dropdown2:
        selected_dropdown2 = df[selected_dropdown].unique()

    filtered_df = df[df[selected_dropdown].isin(selected_dropdown2)]
    pie_chart_figure = px.pie(filtered_df, names=selected_dropdown, values='Currency', title=f'Total Currency Spent by {selected_dropdown}')
    return pie_chart_figure

# Callback for updating line chart based on selected date range
@app.callback(
    Output('line-chart', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_line_chart(start_date, end_date):
    filtered_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    line_chart_figure = px.line(filtered_df, x='Date', y='Currency', title='Total Currency Spent Over Time')
    return line_chart_figure

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




