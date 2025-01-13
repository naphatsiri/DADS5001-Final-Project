import time
import os
import joblib
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import PIL.Image

# Set page configuration
st.set_page_config(
    page_title="AI Recommendation",
    page_icon="💸",
    layout="wide"
)

st.logo("C:/Users/bchan/Final_project/Fundamentor_logo.png", size = "large")

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

new_chat_id = f'{time.time()}'
MODEL_ROLE = 'ai'
AI_AVATAR_ICON = '💵'

# Load the generative model
st.session_state.model = genai.GenerativeModel('gemini-pro')

# Create data/ folder if it doesn't exist
os.makedirs('data/', exist_ok=True)

# Load past chats (if available)
try:
    past_chats = joblib.load('data/past_chats_list')
except:
    past_chats = {}

# Sidebar for past chats
with st.sidebar:
    st.write('# Past Chats')
    if st.session_state.get('chat_id') is None:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id] + list(past_chats.keys()),
            format_func=lambda x: past_chats.get(x, 'New Chat'),
            placeholder='_',
        )
    else:
        st.session_state.chat_id = st.selectbox(
            label='Pick a past chat',
            options=[new_chat_id, st.session_state.chat_id] + list(past_chats.keys()),
            index=1,
            format_func=lambda x: past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
            placeholder='_',
        )
    st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'

# Main app header
st.write('# 🤖 Fundamentor Assistant')
st.write('### Welcome to Fundamentor Your AI Financial Assistant')
st.markdown("---")

# First Section: AI Recommendation Buttons
st.write('## AI Recommendations')
st.write('##### Choose the guidance you need !')
st.markdown("")

col1, col2 = st.columns(2)
with col1:
    st.write('### 📈 Investment Recommendation')
    st.write('Smart, personalized investment advice')
    if st.button('Click here 📈'):
        # Use user_data from Home.py stored in st.session_state
        user_data = st.session_state.get('user_data', {})
        prompt = (
            "Based on the following user data: \n"
            f"- Salary: ฿{user_data.get('salary', 'N/A')}\n"
            f"- Tax Rate: {user_data.get('tax_rate', 'N/A') * 100}%\n"
            f"- Monthly Rental: ฿{user_data.get('monthly_rental', 'N/A')}\n"
            f"- Monthly Food: ฿{user_data.get('monthly_food', 'N/A')}\n"
            f"- Monthly Transport: ฿{user_data.get('monthly_transport', 'N/A')}\n"
            f"- Monthly Utilities: ฿{user_data.get('monthly_utilities', 'N/A')}\n"
            f"- Monthly Entertainment: ฿{user_data.get('monthly_entertainment', 'N/A')}\n"
            f"- Other Expenses: ฿{user_data.get('Other Expense', 'N/A')}\n"
            "Provide a tailored investment recommendation."
        )
        response = st.session_state.model.start_chat().send_message(prompt)
        st.write('### AI Response: Investment Recommendation')
        st.write(response.text)
    

with col2:
    st.write('### 📉 Tax Recommendation')
    st.write('Efficient tax palnning tips')
    if st.button('Click here 📉'):
        # Use user_data from Home.py stored in st.session_state
        user_data = st.session_state.get('user_data', {})
        prompt = (
            "Based on the following user data: \n"
            f"- Salary: ฿{user_data.get('salary', 'N/A')}\n"
            f"- Tax Rate: {user_data.get('tax_rate', 'N/A') * 100}%\n"
            f"- Monthly Rental: ฿{user_data.get('monthly_rental', 'N/A')}\n"
            f"- Monthly Food: ฿{user_data.get('monthly_food', 'N/A')}\n"
            f"- Monthly Transport: ฿{user_data.get('monthly_transport', 'N/A')}\n"
            f"- Monthly Utilities: ฿{user_data.get('monthly_utilities', 'N/A')}\n"
            f"- Monthly Entertainment: ฿{user_data.get('monthly_entertainment', 'N/A')}\n"
            f"- Other Expenses: ฿{user_data.get('Other Expense', 'N/A')}\n"
            "Provide a personalized tax recommendation."
        )
        response = st.session_state.model.start_chat().send_message(prompt)
        st.write('### AI Response: Tax Recommendation')
        st.write(response.text)
    
st.markdown("---")
st.write('### More')
st.write('Not sure where to start? Ask about budgeting, investing, or financial tips now !')


# Manage chat history
try:
    st.session_state.messages = joblib.load(f'data/{st.session_state.chat_id}-st_messages')
    st.session_state.gemini_history = joblib.load(f'data/{st.session_state.chat_id}-gemini_messages')
except:
    st.session_state.messages = []
    st.session_state.gemini_history = []

st.session_state.chat = st.session_state.model.start_chat(history=st.session_state.gemini_history)

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(name=message['role'], avatar=message.get('avatar')):
        st.markdown(message['content'])

# React to user input in the chat interface
if user_message := st.chat_input('Your message here...'):
    with st.chat_message('user'):
        st.markdown(user_message)
    st.session_state.messages.append({'role': 'user', 'content': user_message})

    ai_response = st.session_state.chat.send_message(user_message, stream=True)

    with st.chat_message(name=MODEL_ROLE, avatar=AI_AVATAR_ICON):
        message_placeholder = st.empty()
        full_response = ''
        for chunk in ai_response:
            for ch in chunk.text.split(' '):
                full_response += ch + ' '
                time.sleep(0.05)
                message_placeholder.write(full_response + '▌')
        message_placeholder.write(full_response)

    st.session_state.messages.append({'role': MODEL_ROLE, 'content': full_response, 'avatar': AI_AVATAR_ICON})
    st.session_state.gemini_history = st.session_state.chat.history

    joblib.dump(st.session_state.messages, f'data/{st.session_state.chat_id}-st_messages')
    joblib.dump(st.session_state.gemini_history, f'data/{st.session_state.chat_id}-gemini_messages')

