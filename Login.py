import pickle
from pathlib import Path
from llama_index import LLMPredictor, PromptHelper, ServiceContext
from langchain.chat_models import ChatOpenAI
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.indices.postprocessor import SimilarityPostprocessor
from llama_index import StorageContext, load_index_from_storage
import os
import openai
import json, time
from streamlit_chat import message
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import Email_temp_pass as eml

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Bot Alex", page_icon="🤖")

####################################################################    
# --- USER AUTHENTICATION ---
import yaml
from yaml.loader import SafeLoader
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

st.title("Welcome to BOT Alex 🤖 ")

def user_login ():
    name, authentication_status, username = authenticator.login("Login", 'main')

    if authentication_status == False:
        st.error ("Username/Password is incorrect")
        try:
            username_forgot_pw, email_forgot_password, random_password = authenticator.forgot_password('Forgot password')
            if username_forgot_pw:
                # st.write(email_forgot_password, random_password)
                email = email_forgot_password
                new_password = random_password
                hased_pass = stauth.Hasher([new_password]).generate()
                eml.sendemail(new_password, email)
                st.write (random_password)
                st.write (hased_pass)
                st.write (config)
                with open('./config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.success('New password sent securely')
            # Random password to be transferred to user securely
            else:
                st.error('Username not found')
        except Exception as e:
            st.error(e)

    if authentication_status == None:
        st.warning ('please enter your username and password')

    if authentication_status == True:
        # # ---- SIDEBAR ----
        st.sidebar.title(f"Welcome {name}")
        # st.sidebar.header("select page here :")
        st.session_state.authentication_status = authentication_status
        st.session_state.authenticator = authenticator
        #     try:
        #         if authenticator.reset_password(username, 'Reset password'):
        #             st.success('Password modified successfully')
        #     except Exception as e:
        #         st.error(e)

        ###---- HIDE STREAMLIT STYLE ----


    authenticator.logout("Logout", "sidebar")

user_login()
    