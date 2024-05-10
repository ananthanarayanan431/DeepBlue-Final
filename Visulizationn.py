import streamlit as st
import pandas as pd
import plotly.graph_objects as go

import requests
import yfinance as yf
import matplotlib.pyplot as plt


# Function to get the ticker symbol from the company name
def visulizationn():
    def get_ticker(company_name):
        if not company_name:
            return None
        url = "https://query2.finance.yahoo.com/v1/finance/search"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        params = {"q": company_name, "quotes_count": 1, "country": "India"}

        try:
            res = requests.get(url=url, params=params, headers={'User-Agent': user_agent})
            res.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            data = res.json()

            # Check if 'quotes' key exists and has at least one item
            if 'quotes' in data and data['quotes']:
                company_code = data['quotes'][0]['symbol']
                return company_code
            else:
                st.error("No matching company found.")
                return None
        except requests.exceptions.RequestException as e:
            st.error(f"Error occurred while fetching data: {e}")
            return None

    # Function to generate line chart for high, low, and opening stock values
    # def generate_line_chart(output):
    #     fig = go.Figure()
    #     fig.add_trace(go.Scatter(x=output.index, y=output['High'], mode='lines+markers', name='High', line=dict(color='green')))
    #     fig.add_trace(go.Scatter(x=output.index, y=output['Low'], mode='lines+markers', name='Low', line=dict(color='red')))
    #     fig.add_trace(go.Scatter(x=output.index, y=output['Open'], mode='lines+markers', name='Open', line=dict(color='blue')))
    #     fig.update_layout(title='Line Chart for High, Low, and Open Prices', xaxis_title='Date', yaxis_title='Price')
    #     st.plotly_chart(fig)

    # Function to generate volume chart
    def generate_volume_chart(output):
        fig = go.Figure()
        fig.add_trace(go.Bar(x=output.index, y=output['Volume'], name='Volume'))
        fig.update_layout(title='Volume Chart', xaxis_title='Date', yaxis_title='Volume')
        st.plotly_chart(fig)

    def generate_candlestick_chart(output):
        fig = go.Figure(
            data=[go.Candlestick(x=output.index, open=output['Open'], high=output['High'], low=output['Low'],
                                 close=output['Close'])])
        fig.update_layout(title='Candlestick Chart', xaxis_title='Date', yaxis_title='Price')
        st.plotly_chart(fig)

    def generate_ebitda_chart(ebitda):
        fig = go.Figure()
        fig.add_trace(go.Bar(x=ebitda.index, y=ebitda.values, name='EBITDA'))
        fig.update_layout(title='EBITDA Chart', xaxis_title='Date', yaxis_title='EBITDA')
        st.plotly_chart(fig)

    def generate_revenue_growth_chart(revenue):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=revenue.index, y=revenue.values, mode='lines+markers', name='Total Revenue',
                                 line=dict(color='blue')))
        fig.update_layout(title='Total Revenue Over Time', xaxis_title='Date', yaxis_title='Total Revenue')
        st.plotly_chart(fig)

    def generate_total_expenses_chart(expense):
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=expense.index, y=expense.values, mode='lines+markers', name='Total Expenses',
                                 line=dict(color='red')))
        fig.update_layout(title='Total Expenses Over Time', xaxis_title='Date', yaxis_title='Total Expenses')
        st.plotly_chart(fig)

    # Streamlit app
    st.title('Stock Data Visualization')

    # Sidebar for input and options
    st.sidebar.title('Options')
    company_name = st.sidebar.text_input('Enter company name')
    # generate_line = st.sidebar.checkbox('Generate Line Chart')
    generate_volume = st.sidebar.checkbox('Generate Volume Chart')
    generate_candlestick = st.sidebar.checkbox('Generate Candle Chart')
    generate_ebitda = st.sidebar.checkbox('Generate EBITDA Chart')
    generate_revenue_growth = st.sidebar.checkbox('Generate Revenue Growth Chart')
    generate_total_expenses = st.sidebar.checkbox('Generate Total Expenses Chart')

    # Display the ticker symbol
    if company_name:
        company_ticker = get_ticker(company_name)
        if company_ticker:
            st.sidebar.info(f"Ticker Symbol: {company_ticker}")
        stock = yf.Ticker(company_ticker)

    # Load data and generate charts based on user selection
    if generate_volume:
        output = stock.history(period="1mo")

    if generate_candlestick:
        output = stock.history(period="1mo")

    if generate_ebitda:
        qf = stock.quarterly_financials
        ebitda = qf.loc['EBITDA']

    if generate_revenue_growth:
        income_statement = stock.income_stmt
        revenue = income_statement.loc['Total Revenue']

    if generate_total_expenses:
        income_statement = stock.income_stmt
        expenses = income_statement.loc['Total Expenses']

    if generate_volume:
        generate_volume_chart(output)
    if generate_candlestick:
        generate_candlestick_chart(output)
    if generate_ebitda:
        generate_ebitda_chart(ebitda)
    if generate_revenue_growth:
        generate_revenue_growth_chart(revenue)
    if generate_total_expenses:
        generate_total_expenses_chart(expenses)