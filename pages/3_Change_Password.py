from streamlit_chat import message
import streamlit as st  # pip install streamlit
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
import bcrypt
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

if st.session_state.username:
    username = st.session_state.username
    name = st.session_state.name
    # authenticator = st.session_state.authenticator
    authentication_status = st.session_state.authentication_status
    # Check if username is valid
    if authentication_status:
        try:
            if  authenticator.reset_password(username, 'Change password'):
                with open('./config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                st.success('Password modified successfully')
        except Exception as e:
            st.error(e)

    st.sidebar.title(f"Welcome {name}")
    authenticator.logout("Logout", "sidebar")
    # st.write(authenticator.credentials['usernames']['dedric'])
else:
    # Display message asking user to login first
    st.write("# Please login first")


###---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
