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
company_name = st.text_input("Company Name:", placeholder="perferably url",value="")
role=st.text_input("Role:", placeholder="eg: developer,analyst",value="")
domain=st.text_input("Sector:", placeholder="eg: Education,Legal,Security",value="")
specific=st.text_input("Specific Feature:", placeholder="eg: Customer support",value="")
company_size = st.selectbox(
    "Number Of Employees:",
    ["", "1-100", "101-1000", "1000+"],
    format_func=lambda x: "Select" if x == "" else str(x)
)
waste=st.text_input("Product/Category:",placeholder="DataDogs")

def read_json_file(file_path):
    """Read the input JSON file and return its contents."""
    with open(file_path, 'r',encoding='utf-8') as f:
        return json.load(f)

if st.button("Fetch the relevant reviews"):
    with st.spinner('Fetching reviews matching the profile'):
        time.sleep(5)
    with open('customer.json', 'r') as f:
        data=json.load(f)
    chunks=[]
    for item in data:
        if item['useful']=='0' and item['customer_useful']=='0':
            chunks.append(item['body'])
    refined_chunks=[]
    for i in range(len(chunks)):
        refined_chunks.append(Document(page_content=str(chunks[i])))
    st.markdown("""
### Pros and Cons 


##### Pros:

- **Device Management/Endpoint Management:**
    - Offers comprehensive management of Apple devices, crucial for maintaining security and efficiency in a large fintech company.
    - Supports dynamic policy adjustments and centralized endpoint deployment, enhancing operational flexibility and user satisfaction.
    - Near zero-touch deployment reduces setup time, benefiting both IT teams and end-users.
                        
- **Remote Assistance:**
    - Facilitates remote app management and real-time support, minimizing the need for physical device handling.
    - Reliable MDM solution, particularly effective in cloud environments, with Jamf Connect simplifying password management.
                
- **Patch Management:**
    - Ensures timely updates and compliance, critical for security in the fintech sector.
    - Provides robust monitoring and reporting on device compliance, enhancing overall security posture.
                
- **Support and Community:**
    - Strong support network and an active community for knowledge sharing and troubleshooting.
    - Jamf Nation community serves as a valuable resource for collaboration and problem-solving.
                
##### Cons:

- **Technical Debt and Console Limitations:**
    - The management console has accumulated technical debt, with outdated features and quirks affecting usability.
    - Slow monitoring of policy and application deployment can hinder efficiency.
                
- **Reporting and SIEM Integration:**
    - Limited built-in reporting capabilities and lack of SIEM integration may pose challenges for compliance-heavy environments.
                
- **Learning Curve:**
    - Steep initial learning curve, though proficiency simplifies device management tasks.
                
- **Cost Considerations:**
    - High costs associated with the platform, especially concerning unmanaged devices, can impact budget-conscious IT departments.
""")
    st.markdown("________________________________")
    st.markdown("""
### Summary:

For an IT Manager in the fintech sector managing a company with over 1000 employees, **Jamf Pro** offers a comprehensive suite of features focused on device management, remote assistance, and patch management, specifically tailored for Apple devices. The platform excels in efficiently managing a large fleet of devices, allowing for dynamic and automated configuration applications, which significantly reduces manual workload. 

Jamf Pro's remote assistance capabilities facilitate efficient device management without the need for physical interaction, and its patch management system ensures devices are consistently updated with the latest software and OS patches. The platform also benefits from a user-friendly interface and a supportive community, which aids in troubleshooting and knowledge sharing. 

However, challenges such as a steep learning curve, technical debt in the management console, and limited reporting capabilities can pose difficulties. Despite these challenges, **Jamf Pro** remains a reliable and user-friendly solution for organizations heavily invested in Apple ecosystems.



##### Fitment Rating: 8/10

##### Reason for Rating:

Jamf Pro is a strong fit for an IT Manager in a large fintech company due to its robust device management capabilities, effective remote assistance, and efficient patch management features. These strengths align well with the needs of managing a large fleet of Apple devices, reducing IT workload, and ensuring high compliance rates. 

However, the platform's steep learning curve and technical debt in the management console slightly hinder its overall fitment, preventing a perfect score. Despite these drawbacks, its strengths in remote management, community support, and cloud integration make it a valuable tool for the specified customer profile.
""")
    st.markdown("______________________")
    st.header("Reviews that matches your profile")
    with open("customer.json", "r") as json_file:
        file = json.load(json_file)
    for elem in file:
        flag=0
        if elem['useful'] == '0' and elem['customer_useful']=='0':  # Display reviews marked as '0'
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
    
