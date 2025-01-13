import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(
    page_title="Personal Financial Planning Dashboard",
    page_icon="🤖",
    layout="wide"
)

st.logo("C:/Users/bchan/Final_project/Fundamentor_logo.png", size = "large")

# Header Section
st.title("📊 Personal Financial Planning Summary")
st.subheader("Your Financial Overview at a Glance")

st.markdown("---")

# Pie Chart for Financial Distribution
if 'user_data' in st.session_state:
    user_data = st.session_state['user_data']
    
    # Convert the user_data dictionary to a DataFrame
    data = {
        "Category": ["Rental", "Food", "Transport", "Utilities", "Entertainment","Other Expense"],
        "Amount": [
            user_data.get('monthly_rental', 0),
            user_data.get('monthly_food', 0),
            user_data.get('monthly_transport', 0),
            user_data.get('monthly_utilities', 0),
            user_data.get('monthly_entertainment', 0),
            user_data.get('Other Expense', 0),
        ],
    }
    df = pd.DataFrame(data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Financial Distribution")
        fig_pie = px.pie(df, names="Category", values="Amount", 
                         title="Breakdown of Your Finances", 
                         color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Bar Chart for Financial Overview
    with col2:
        st.markdown("### Financial Overview")
        fig_bar = px.bar(df, x="Category", y="Amount", color="Category",
                         title="Expenses by Category",
                         text_auto=True, color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_bar, use_container_width=True)

    net_salary = user_data.get("salary", 0) * (1 - user_data.get("tax_rate", 0))
total_expenses = (
    user_data.get("monthly_rental", 0)
    + user_data.get("monthly_food", 0)
    + user_data.get("monthly_transport", 0)
    + user_data.get("monthly_utilities", 0)
    + user_data.get("monthly_entertainment", 0)
    + user_data.get("Other Expense", 0)
)

# Prepare data for the pie chart
data = {
    "Category": ["Net Salary", "Total Expenses"],
    "Amount": [net_salary, total_expenses],
}
df = pd.DataFrame(data)

st.markdown("---")

# Stack Bar-Chart for Salary vs Expense
st.title("💰 Salary vs Expenses Breakdown")
import streamlit as st
import plotly.graph_objects as go

# Initialize session state for sliders
if "emergency_fund_percent" not in st.session_state:
    st.session_state.emergency_fund_percent = 50
if "retirement_fund_percent" not in st.session_state:
    st.session_state.retirement_fund_percent = 50

# Function to synchronize sliders
def sync_emergency_fund():
    st.session_state.retirement_fund_percent = 100 - st.session_state.emergency_fund_percent

def sync_retirement_fund():
    st.session_state.emergency_fund_percent = 100 - st.session_state.retirement_fund_percent

if 'user_data' in st.session_state:
    user_data = st.session_state['user_data']
    
    # Extract data
    salary = user_data['salary']
    expenses = {
        'Tax': salary * (user_data['tax_rate'] / 100),  # Calculate tax based on percentage
        'Rent': user_data['monthly_rental'],
        'Food': user_data['monthly_food'],
        'Transport': user_data['monthly_transport'],
        'Utilities': user_data['monthly_utilities'],
        'Entertainment': user_data['monthly_entertainment'],
        'Other': user_data['Other Expense'],
    }

    total_expense = sum(expenses.values())  # Total expenses

    # Financial Goals and Progress
    tax = salary * (user_data['tax_rate'] / 100)
    savings_after_tax = salary - tax - total_expense  # Calculate savings after tax

    # Sidebar with Filters
    st.sidebar.title("Customize Your Saving Plan")
    st.sidebar.markdown("Use the filters below to tailor the dashboard:")

    # Linked sliders for Emergency Fund and Retirement Fund
    emergency_fund_percent = st.sidebar.slider(
        "Emergency Fund Allocation %", 
        min_value=0, max_value=100, 
        value=st.session_state.emergency_fund_percent, 
        step=5, 
        key="emergency_fund_percent", 
        on_change=sync_emergency_fund
    )

    retirement_fund_percent = st.sidebar.slider(
        "Retirement Fund Allocation %", 
        min_value=0, max_value=100, 
        value=st.session_state.retirement_fund_percent, 
        step=5, 
        key="retirement_fund_percent", 
        on_change=sync_retirement_fund
    )

    # Calculate predicted savings from savings after tax
    emergency_fund_savings = savings_after_tax * (emergency_fund_percent / 100)
    retirement_fund_savings = savings_after_tax * (retirement_fund_percent / 100)

    # Define goals
    goals = ["Emergency Fund", "Retirement Savings"]
    types = ["Savings After Tax", "Predicted Savings"]

    # Prepare data for the cluster-column chart
    data = {
        "Goal": ["Emergency Fund"] * 2 + ["Retirement Savings"] * 2,
        "Type": types * 2,
        "Amount": [savings_after_tax, emergency_fund_savings, savings_after_tax, retirement_fund_savings]
    }
    df = pd.DataFrame(data)

    # Create a grouped bar chart
    fig_goals = px.bar(
        df,
        x="Goal",
        y="Amount",
        color="Type",
        barmode="group",
        title="Comparison of Savings After Tax vs Predicted Savings by Goal",
        text="Amount",
        color_discrete_map={
            "Savings After Tax": "green",
            "Predicted Savings": "blue"
        }
    )

    fig_goals.update_traces(textposition="outside")
    fig_goals.update_layout(
        xaxis_title="Financial Goals",
        yaxis_title="Amount (฿)",
        legend_title="Savings Type"
    )

    # Display the chart
    st.plotly_chart(fig_goals, use_container_width=True)

else:
    st.warning("No user data found. Please enter and save your data first.")

# Footer
st.markdown("---")
st.caption("© 2024 Fundamentor. All rights reserved.")




