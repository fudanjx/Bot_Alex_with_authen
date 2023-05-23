
from llama_index import (
    GPTVectorStoreIndex,
    ResponseSynthesizer,
    SimpleDirectoryReader,
    load_index_from_storage,
    StorageContext,
)
from llama_index.retrievers import VectorIndexRetriever
from llama_index import LLMPredictor, PromptHelper, ServiceContext
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.indices.postprocessor import SimilarityPostprocessor
from llama_index.vector_stores.faiss import FaissVectorStore
from langchain.chat_models import ChatOpenAI
import os 
import openai 
import json 
import logging 
import sys 
import streamlit as st
from streamlit_chat import message
import shutil

if st.session_state.username:
    username = st.session_state.username
    name = st.session_state.name
    ##############################################
    def open_file(filepath):
        with open(filepath, 'r') as infile:
            return infile.read()

    openai.api_key = open_file('./data/openaiapikey.txt')          
    os.environ['OPENAI_API_KEY'] = openai.api_key      

    #Creating the chatbot interface

    st.title("Build Your Personal Chat Bot")

    #######################################################
    @st.cache_resource
    def build_index(docs):
        # define LLM
        llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name ="gpt-3.5-turbo", streaming=True))
        service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, chunk_size_limit=512)
        index = GPTVectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

    def main():
        st.write("#### upload your documents here")
        chatbot_name = st.text_input("Enter Chatbot Name")
        if not chatbot_name:
            st.warning("Please enter a chatbot name before uploading files.")
            return
        uploaded_files = st.file_uploader("Upload Files", accept_multiple_files=True)
        if uploaded_files:
            source_path = os.path.join(os.getcwd(), "temp")
            if not os.path.exists(source_path):
                os.makedirs(source_path)
            for uploaded_file in uploaded_files:
                with open(os.path.join(source_path, uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
            docs = SimpleDirectoryReader(source_path).load_data()
            progress_text = 'building ...'
            my_bar = st.progress(0, text=progress_text)
            for percent_complete in range(100):
                index = build_index(docs)
                my_bar.progress(percent_complete + 1, text=progress_text)      
            index.storage_context.persist(os.path.join(os.getcwd(), ".", "users", username, "db", chatbot_name))
            st.success("Index created and saved successfully!")



    def delete_bot():
        st.write("#### please delete your bot here")
        try: 
            bot_list = os.listdir(os.path.join(os.getcwd(), ".", "users", username, "db"))
            bot_name = st.selectbox("Select Your Bot to delete", bot_list)
            if st.button("Delete Bot"):
                bot_path = os.path.join(os.getcwd(), ".", "users", username,"db", bot_name)
                shutil.rmtree(bot_path)
                st.success(f"{bot_name} has been deleted successfully!")
        except FileNotFoundError as e:
            st.write('#### Build your first bot first') 


    if __name__ == "__main__":
        col1, col2 = st.columns(2)
        with col1:
            main()
        with col2:
            delete_bot()
    st.sidebar.title(f"Welcome {name}")
    authenticator = st.session_state.authenticator 
    authenticator.logout("Logout", "sidebar")
else:
    st.write("## Please login first")

###---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)