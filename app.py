import streamlit as st
import pandas as pd
import tweepy
from streamlit.components.v1 import html
import streamlit.components.v1 as components
import requests
from functions import extract_all_tweets, extract_threads, convert_df, theTweet

######################### Keys #########################################

consumer_key = st.secrets["consumer_key"]
consumer_secret = st.secrets["consumer_secret"]
access_token = st.secrets["access_token"]
access_token_secret = st.secrets["access_token_secret"]

######################### Tkns #########################################

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
if 'api' not in st.session_state:
    api = tweepy.API(auth)
    st.session_state['api'] = api

########################################################################


st.set_page_config(page_title="Twitter Thread Extractor")
html_temp = """
                    <div style="background-color:{};padding:1px">
                    
                    </div>
                    """

button = """
<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="nainiayoub" data-color="#5F7FFF" data-emoji=""  data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#ffffff" data-coffee-color="#FFDD00" ></script>
"""

hide="""
<style>
footer{
	visibility: hidden;
    	position: relative;
}
.viewerBadge_container__1QSob{
    visibility: hidden;
}

<style>
"""
st.markdown(hide, unsafe_allow_html=True)



st.markdown("<h1 style='text-align: center'><span style='color: #1DA1F2'>Twitter</span> Thread Extractor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center'>Extracting Twitter threads from Twitter profiles.</p>", unsafe_allow_html=True)

username = st.text_input("Enter Twitter username", placeholder="Twitter username", disabled=False)
# 


st.markdown(
    """
    <style>
        iframe[width="220"] {
            position: fixed;
            bottom: 60px;
            right: 40px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if username:
    df = extract_all_tweets(username)
    if not df.empty:
        df_threads = extract_threads(df, username)
        message = str(len(list(df_threads['Thread URL'])))+" threads by @"+username
        
        # section 1: Download threads 
        
        st.markdown("""
        ### Download threads
        """)
        st.info(message)
        with st.expander("Your extracted Twitter threads"):
            st.dataframe(df_threads)

            csv = convert_df(df_threads)
            file_name_value = username+"_threads.csv"

        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=file_name_value,
            mime='text/csv',
        )

        # section 2: display threads

        st.markdown("""
        ### Display threads
        """)
        url_threads = list(df_threads['Thread URL']) 
        option = st.selectbox("Choose your Twitter thread", url_threads)
        res = theTweet(option)
        components.html(res, height=700)
else:
    st.markdown('''
    <a target="_blank" style="color: black" href="https://www.github.com/nainiayoub">
        <button class="btn-github">
            <i>GitHub</i>
        </button>
    </a>

    <a target="_blank" style="color: black" href="https://twitter.com/nainia_ayoub">
        <button class="btn-twitter">
            <i>Twitter</i>
        </button>
    </a>
    


    <style>
    .btn-github{
        display: inline-flex;
        -moz-box-align: center;
        align-items: center;
        -moz-box-pack: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        margin: 0px;
        line-height: 1.6;
        color: #fff;
        text-weight: bold;
        background-color: #000 ;
        width: auto;
        user-select: none;
        border: 1px solid #000 ;
        }
    .btn-github:hover{
        color: #000 ;
        background-color: #fff;
    }
    .btn-linkedin{
        display: inline-flex;
        -moz-box-align: center;
        align-items: center;
        -moz-box-pack: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        margin: 0px;
        line-height: 1.6;
        color: #000;
        text-weight: bold;
        background-color: #f7d501 ;
        width: auto;
        user-select: none;
        border: 1px solid #f7d501 ;
        }
    .btn-linkedin:hover{
        color: #f7d501 ;
        background-color: #fff;
    }
    .btn-twitter{
        display: inline-flex;
        -moz-box-align: center;
        align-items: center;
        -moz-box-pack: center;
        justify-content: center;
        font-weight: 400;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        margin: 0px;
        line-height: 1.6;
        color: #fff;
        text-weight: bold;
        background-color: rgb(29, 161, 242) ;
        width: auto;
        user-select: none;
        border: 1px solid rgb(29, 161, 242) ;
        }
    .btn-twitter:hover{
        color: rgb(29, 161, 242) ;
        background-color: #fff;
    }
    </style>
    ''',
    unsafe_allow_html=True
    )
        
