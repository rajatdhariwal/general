import openai
import json
import streamlit as st
from langchain.llms import OpenAIChat
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain_core.documents import Document
import os
import time
import re

st.markdown(
    """
    <style>
    .jazzee-title {
                    display: inline;
                    background: linear-gradient(93.59deg, orange 3.13%, #f6be58 85.77%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    font-size: 1em;
                    font-weight: bold;
    }
    </style>
    """, 
    unsafe_allow_html=True
)
st.markdown('<h1><span class="jazzee-title">Jazzee</span> Assist</h1>', unsafe_allow_html=True)
company_name = st.text_input("Company Name:", placeholder="eg: www.greenlight.com",value="")
role=st.text_input("Role:", placeholder="eg: IT Manager",value="")
domain=st.text_input("Sector:", placeholder="eg: Fintech",value="")
specific=st.text_input("Specific Feature:", placeholder="eg: Device Management",value="")
company_size = st.selectbox(
    "Number Of Employees:",
    ["", "1-100", "101-1000", "1000+"],
    format_func=lambda x: "Select" if x == "" else str(x)
)
waste=st.text_input("Product/Category:",placeholder="eg: JAMF")
st.subheader("💬 **Suggested Queries**")
# Initialize session states for each button to track if they were clicked
if "review_buttons" not in st.session_state:
    st.session_state.review_buttons = {
        "IT Manager for JAMF": False,
        "Marketing Head for Mixpanel": False,
        "CISO for Vanta Software": False,
        "CTO for New Relic": False,
    }

if "fetch_button_clicked" not in st.session_state:
    st.session_state.fetch_button_clicked = False

# Function to mark a specific review button as clicked
def set_review_button_red(button_name):
    st.session_state.review_buttons[button_name] = True

# CSS to ensure consistent button size across all buttons
button_css = """
<style>
button {
    width: 100%;  /* Make the button take full width of the column */
    height: 50px;
    font-size: 16px;
    border-radius: 8px;
    border: 2px solid red;
    cursor: pointer;
    color: black;
    transition: 0s;
}

button:hover {
    background-color: white;
    color: white;
}
</style>
"""
# Inject CSS into the app
st.markdown(button_css, unsafe_allow_html=True)

# Create four columns (one for each button) to align them horizontally
cols = st.columns(len(st.session_state.review_buttons))

# Display the buttons in their respective columns
for (button_name, clicked), col in zip(st.session_state.review_buttons.items(), cols):
    with col:
        if clicked:
            # Render as a red-styled HTML button
            st.markdown(f'<button>{button_name}</button>', unsafe_allow_html=True)
        else:
            # Render a Streamlit button and set it as clicked when pressed
            if st.button(button_name, key=button_name, on_click=set_review_button_red, args=(button_name,)):
                st.session_state.review_buttons[button_name] = True

def read_json_file(file_path):
    """Read the input JSON file and return its contents."""
    with open(file_path, 'r',encoding='utf-8') as f:
        return json.load(f)

def linkify_numbers(numbers):
    return ", ".join([f"[{num}](#{num})" for num in numbers])

if st.button("Fetch the relevant reviews"):
    with st.spinner('⏳ Fetching reviews matching the profile'):
        time.sleep(5)
    st.markdown("""
##### Fitment Rating: 8/10""")
    with st.expander("##### Reason for Rating:"):
        st.markdown("""
    Jamf is a powerful MDM solution for managing Apple devices, offering extensive features and strong integration capabilities. However, its steep learning curve, inconsistent support, and scalability issues may pose challenges for larger organizations or those with complex compliance needs. While it excels in remote management and security, potential customers should weigh these pros and cons against their specific organizational requirements and consider the competitive landscape before making a decision.
    """)
    with st.expander("Pros"):
        st.write(f"""
        - **Comprehensive Apple Device Management** {linkify_numbers([0, 2, 7, 18, 41])}.
        - **High Reliability in Large-Scale Environments** {linkify_numbers([3, 4, 7, 10, 11, 23])}.
        - **Strong Customer Support and Community** {linkify_numbers([5, 11, 35, 36, 50])}
        - **Efficient Zero-Touch Deployment** {linkify_numbers([0, 3, 5, 44, 45])}.
        - **Integrated Security Features** {linkify_numbers([2, 4, 10, 30, 43])}.
        """)

    with st.expander("Cons"):
        st.write(f"""
        - **Steep Learning Curve** {linkify_numbers([2, 11, 17, 34, 35])}.
        - **High Cost for Advanced Features** {linkify_numbers([0, 5, 14, 15, 49])}.
        - **Outdated User Interface** {linkify_numbers([4, 11, 24, 36, 50])}.
        - **Inconsistent Patch Management** {linkify_numbers([1, 15, 23, 28, 50])}.
        - **Limited Remote Assistance Capabilities** {linkify_numbers([14, 15, 28, 50])}.
        """)

    st.markdown("______________________")
    st.header("Reviews that matches your profile")
    with open("clean_rev.json", "r") as json_file:
        file = json.load(json_file)
    for idx, elem in enumerate(file):
        flag=0
        if elem['useful'] == '0' and elem['customer_useful'] == '0':  # Display reviews marked as '0'
            st.markdown(f'<a name="{idx}"></a>', unsafe_allow_html=True)  # Create an anchor for each review
        if elem['body']=="":
            flag=1
        if 'title' in elem and flag==0:
            st.subheader(elem['title'])
        if 'platform' in elem:
            if 'upvotes' in elem:
                st.markdown(f"Platform : {elem['platform']} | {elem['created'].split()[0]} | [Open Review]({elem['url']}) | Upvotes : {elem['upvotes']}")
            else:
                st.markdown(f"Platform : {elem['platform']} | [Open Review]({elem['url']})")
        else:   
            st.markdown(f"Platform : Reddit/{elem['subreddit']} | {elem['created'].split()[0]} | [Open Review]({elem['url']}) | Upvotes : {elem['upvotes']}")
        sample_para=elem['body']
        if flag==1:
            sample_para=elem['title']
        para = sample_para.replace('\n', '<br>')
        if elem['sentiment']=='2':
            st.markdown(
                        f"""
                        <div style="background-color: #d4edda; padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                            <p style="color: #155724; font-size: 16px; margin: 0;">{para}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        elif elem['sentiment']=='4':
            st.markdown(
                        f"""
                        <div style="background-color: #cce5ff; padding: 10px; border-radius: 5px;">
                            <p style="color: #004085; font-size: 16px;">{para}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        else:
            st.markdown(
                        f"""
                        <div style="background-color: #f8d7da; padding: 10px; border-radius: 5px;">
                            <p style="color: #721c24; font-size: 16px;">{para}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
        st.markdown("______________________")
