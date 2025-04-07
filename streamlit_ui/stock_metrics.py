import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px

def fetch_stock_data(ticker, start_date, end_date):
    """Fetch stock data from Yahoo Finance."""
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        return data if not data.empty else None
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

def get_stock_metrics(ticker, start_date, end_date):
    """Fetch stock data, calculate metrics, and display visualizations."""
    data = None  # Initialize data variable

    if ticker:
        try:
            data = yf.download(ticker, start=start_date, end=end_date)

            if not data.empty:
                st.subheader(f"Stock Data for {ticker}")
                st.write(data)  

                # Check if 'Adj Close' exists, otherwise use 'Close'
                price_column = "Adj Close" if "Adj Close" in data.columns else "Close"

                if isinstance(data.columns, pd.MultiIndex):
                    data.columns = data.columns.droplevel(1)  

                # Plot Stock Price
                fig = px.line(data, x=data.index, y=price_column, title=f"{ticker} Stock Price")
                st.plotly_chart(fig)

            else:
                st.warning("No data available. Please check the ticker symbol and date range")
                data = None  # Set data to None if empty

        except Exception as e:
            st.error(f"Error fetching data: {e}")
            data = None  # Set data to None if empty

    else:
        st.info("Please enter a valid stock ticker")

    # Tabs for additional data
    pricing_data, _ = st.tabs(["Pricing Data"]) 

    with pricing_data:
        st.header('Price Movements')

        if data is not None and not data.empty:
            data["% Change"] = ((data[price_column] / data[price_column].shift(1)) - 1) * 100
            data.dropna(inplace=True)

            st.write(data)

            # Calculate metrics
            annual_return = data["% Change"].mean() * 252
            stdev = np.std(data["% Change"]) * np.sqrt(252)

            st.write(f"**Annual Return:** {annual_return:.2f}%") 
            st.write(f"**Standard Deviation:** {stdev:.2f}%")

            if stdev != 0:
                st.write(f"**Risk-Adjusted Return:** {annual_return / stdev:.2f}")
            else:
                st.write("**Risk-Adjusted Return:** N/A (Standard deviation is zero)")

            # Additional visualizations
            fig_vol = px.bar(data, x=data.index, y="Volume", title=f"{ticker} Trading Volume")
            st.plotly_chart(fig_vol)

        else:
            st.warning("No data available. Please check the ticker symbol and date range")
