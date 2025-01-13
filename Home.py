import streamlit as st
from PIL import Image
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import os


# Set the page configuration
st.set_page_config(
    page_title="Creative Financial Homepage",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.logo("C:/Users/bchan/Final_project/Fundamentor_logo.png", size = "large")
st.image("C:/Users/bchan/Final_project/banner.png", use_container_width=True)

#Welcome Text
st.markdown(
    """
    <div style="text-align: center;">
        <h1>💸 Welcome to Fundamentor 💸</h1>
        <h2>Your Personalized AI-Powered Financial Assistant.</h2>
        <p>We’re here to guide you every step of the way toward financial freedom. Let’s start planning your brighter future today!</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Financial Recommendations
st.markdown("---")
st.header("🔄 What We Offer")

# Images for each section
images = [
    "C:/Users/bchan/Final_project/3.png",  # Budget Tracker image
    "C:/Users/bchan/Final_project/4.png",  # Financial Planning image
    "C:/Users/bchan/Final_project/9.png"   # AI Recommendation image
]

# Create columns
cols = st.columns(3)

# Add images above columns
for i, col in enumerate(cols):
    with col:
        st.image(images[i], use_container_width=True)

# Add content to each column
recommendations = [
    {"title": "Budget Tracker", "desc": "Track your spending. Stay on budget. Save smarter."},
    {"title": "Financial Planning", "desc": "Plan today, Secure tomorrow."},
    {"title": "AI Recommendation", "desc": "Track your spending with ease."}
]

for i, rec in enumerate(recommendations):
    with cols[i % 3]:
        st.subheader(rec["title"])
        st.write(rec["desc"])
        


# Sidebar
st.sidebar.title("Explore More")
st.sidebar.markdown("\n".join([
    "- [Financial Blog](https://www.bloomberg.com/asia)",
    "- [Contact Us](https://as.nida.ac.th/contact-us/)",
    "- [About Us](https://as.nida.ac.th/)"
]))


#st.set_page_config(
#    page_title="Financial Planning Calculator")

st.markdown("---")

st.title("🧮 Start Planning Now!")
st.write("Embark on your journey to lasting wealth.")

st.header("**Income**")
st.subheader("Yearly Income")
colAnnualSal, colTax = st.columns(2)

with colAnnualSal:
    salary = st.number_input("Enter your annual income(฿): ", min_value=0.0, format='%f')
with colTax:
    tax_rate = st.number_input("Enter your tax rate(%): ", min_value=0.0, format='%f')

tax_rate = tax_rate / 100.0
salary_after_taxes = salary * (1 - tax_rate)
monthly_takehome_salary = round(salary_after_taxes / 12.0, 2)

st.header("**Monthly Expenses**")
colExpenses1, colExpenses2 = st.columns(2)

with colExpenses1:
    st.subheader("Monthly Rental")
    monthly_rental = st.number_input("Enter your monthly rental(฿): ", min_value=0.0,format='%f' )
    
    st.subheader("Monthly Food Budget")
    monthly_food = st.number_input("Enter your monthly food budget(฿): ", min_value=0.0,format='%f' )

    st.subheader("Monthly Entertainment Budget")
    monthly_entertainment = st.number_input("Enter your monthly entertainment budget (฿): ", min_value=0.0,format='%f' )  
    
     
with colExpenses2:
    st.subheader("Monthly Transport")
    monthly_transport = st.number_input("Enter your monthly transport fee (฿): ", min_value=0.0,format='%f' )   
    
    st.subheader("Monthly Utilities Fees")
    monthly_utilities = st.number_input("Enter your monthly utilities fees (฿): ", min_value=0.0,format='%f' )
    
    st.subheader("Other Expense")
    other_expense = st.number_input("Enter your monthly other expense (฿): ", min_value=0.0,format='%f' )   

monthly_expenses = monthly_rental + monthly_food + monthly_transport + monthly_entertainment + monthly_utilities + other_expense
monthly_savings = monthly_takehome_salary - monthly_expenses 

st.markdown("---")

st.header("💰**Savings**")
st.markdown(
    f"""
    <div style="font-size: 13pt;">
        <p><strong>Monthly Take Home Salary:</strong> ฿{round(monthly_takehome_salary, 2)}</p>
        <p><strong>Monthly Expenses:</strong> ฿{round(monthly_expenses, 2)}</p>
        <p><strong>Monthly Savings:</strong> ฿{round(monthly_savings, 2)}</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# Save input to session state
if st.button("Save Data"):
    st.session_state['user_data'] = {
        'salary': salary,
        'tax_rate': tax_rate,
        'monthly_rental': monthly_rental,
        'monthly_food': monthly_food,
        'monthly_transport' : monthly_transport,
        'monthly_utilities' : monthly_utilities,
        'monthly_entertainment' : monthly_entertainment,
        'Other Expense' : other_expense
    }
    st.success("Data saved successfully!")

#Link to go to dashboard page
if st.button("Go to Dashboard"):
    if 'user_data' not in st.session_state:
        st.warning("Please save your data before proceeding to the dashboard!")
    else:
        # Navigate to the Dashboard page using experimental_set_query_params
        st.switch_page("C:/Users/bchan/Final_project/pages/1_📊_Dashboard.py")
    # Footer Section
st.markdown("---")
st.caption("© 2024 Fundamentor. All rights reserved.")


