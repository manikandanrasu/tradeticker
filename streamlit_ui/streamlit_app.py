import streamlit as st
from streamlit_option_menu import option_menu

import requests
from datetime import datetime, timedelta

from stock_metrics import fetch_stock_data, get_stock_metrics

# Configure page layout
st.set_page_config(page_title="TradeTicker", layout="wide")

# Sidebar Authentication Forms
with st.sidebar:
    st.image("https://via.placeholder.com/150", width=150)  # Placeholder for logo
    st.title("TradeTicker")

    auth_option = st.radio("Choose an option:", ["Login", "Signup"])

    if auth_option == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username and password:
                data = {
                    "username": username,
                    "password": password
                }

                response = requests.post("http://localhost:5000/login_user", json=data)

                if response.status_code == 200:
                    st.success("Login Successful!")
                else:
                    st.error(f"Login failed: {response.json().get('error')}")
            else:
                st.warning("Please enter both username and password.")

    elif auth_option == "Signup":
        st.subheader("Create an Account")
        new_username = st.text_input("Enter Username")
        email = st.text_input("Email")
        password = st.text_input("Enter Password", type="password")
        
        if st.button("Sign Up"):
            if new_username and email and password:
                data = {
                    "username": new_username,
                    "email": email,
                    "password": password
                }

                try:
                    response = requests.post("http://localhost:5000/signup", json=data)
                    st.write("Raw Response:", response.text)

                    if response.status_code == 200:
                        st.success("User registered successfully!")
                    else:
                        error_msg = response.json().get('error', 'Unknown error occurred')
                        st.error(f"Signup failed: {error_msg}")
                except Exception as e:
                    st.error(f"Request failed: {str(e)}")
            else:
                st.warning("All fields are required.")

# Navigation Menu
selected = option_menu(
    menu_title="TradeTicker",
    options=["Ticker Screener", "About", "Contact"],
    icons=["chart-line", "info-circle", "envelope"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

# Main Content
if selected == "Ticker Screener":
    st.header("Ticker Screener")
    st.markdown("Anlaysis stock trends, returns and financial metrics")

    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL, TSLA)").upper()

    # Default date range (Last 6 months)
    default_start = datetime.today() - timedelta(days=180)
    default_end = datetime.today()

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", default_start)
    with col2:
        end_date = st.date_input("End Date", default_end)

    if start_date >= end_date:
        st.error("Start date must be eariler than end date")

    else:
        if st.button("SUBMIT"):
            data = fetch_stock_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
            if data is not None:
                st.dataframe(data)
            else:
                st.error("No data found for the given inputs")

elif selected == "About":
    st.title("ℹ️ About TradeTicker")
    st.write("TradeTicker provides real-time stock analysis and insights for traders of all levels.")

elif selected == "Contact":
    st.title("📩 Contact Us")
    st.write("📧 Email: support@tradeticker.com")

# Footer
st.markdown("---")
st.markdown("© 2025 TradeTicker | All rights reserved.")
