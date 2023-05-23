from llama_index import LLMPredictor, PromptHelper, ServiceContext
from langchain.chat_models import ChatOpenAI
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.indices.postprocessor import SimilarityPostprocessor
from llama_index import StorageContext, load_index_from_storage
import os
import openai
import json, time
import streamlit as st
from streamlit_chat import message

st.set_page_config(page_title="Chat Now!",page_icon="📈")

if st.session_state.username:
    username = st.session_state.username
    name = st.session_state.name
    try: 
        ##########################################################
        # st.title("Select your Bot, then ASK! ")
        # Show a list of all the chatbot names
        bot_dir = os.path.join(os.getcwd(), "users", username, "db")
        if not os.listdir(bot_dir):
            chatbot_names = ""
        else:
            chatbot_names = os.listdir(bot_dir)
        selected_bot = st.selectbox("#### Select Your Bot", chatbot_names)
        print(bot_dir)
        ##########################################################
        class Chatbot:
            def __init__(self, api_key, index):
                self.index = index
                openai.api_key = api_key
                self.chat_history = []

            def generate_response(self, user_input):
                prompt = "\n".join([f"{message['role']}: {message['content']}" for message in self.chat_history[-5:]])
                prompt += f"\nUser: {user_input}"
                query_engine = index.as_query_engine()
                response = query_engine.query(user_input)
                # response = index.query(user_input)
                # message = {"role": "assistant", "content": response.response}
                message = response.response
            
                self.chat_history.append({"role": "user", "content": user_input})
                self.chat_history.append({"role": "assistant", "content": message})
                return message
            
            def load_chat_history(self, filename):
                try:
                    with open(filename, 'r') as f:
                        self.chat_history = json.load(f)
                except FileNotFoundError:
                    pass

            def save_chat_history(self, filename):
                with open(filename, 'w') as f:
                    json.dump(self.chat_history, f)

        ##########################################################
        def open_file(filepath):
            with open(filepath, 'r') as infile:
                return infile.read()

        openai.api_key = open_file('./data/openaiapikey.txt')          
        os.environ['OPENAI_API_KEY'] = openai.api_key      

        #Creating the chatbot interface
        # Storing the chat
        if 'generated' not in st.session_state:
            st.session_state['generated'] = []

        if 'past' not in st.session_state:
            st.session_state['past'] = []

            # We will get the user's input by calling the get_text function
        def get_text():
            input_text = st.text_input("You: ","", key="input")
            return input_text

        # Rebuild storage context and load index for selected bot
        if not os.listdir(bot_dir):
            st.write("build your bot at Bot Manager page")
        else:
            storage_context = StorageContext.from_defaults(persist_dir= os.path.join(os.getcwd(), "users",username, "db", selected_bot))
            index = load_index_from_storage(storage_context)  
            bot = Chatbot(openai.api_key, index=index)

            user_input = get_text()

            if user_input:
                output = bot.generate_response(user_input)
                # store the output 
                st.session_state.past.append(user_input)
                st.session_state.generated.append(output)


            if st.session_state['generated']:
                
                for i in range(len(st.session_state['generated'])-1, -1, -1):
                    message(st.session_state["generated"][i], key=str(i))
                    message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
        
        st.sidebar.title(f"Welcome {name}")
        authenticator = st.session_state.authenticator 
        authenticator.logout("Logout", "sidebar")
    except FileNotFoundError as e:
        st.write('# Build your first bot in Bot Manager module first') 
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


