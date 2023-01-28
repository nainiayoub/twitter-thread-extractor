import streamlit as st
import pandas as pd
import tweepy
from streamlit.components.v1 import html
import streamlit.components.v1 as components
import requests
from functions import extract_all_tweets, extract_threads, convert_df, theTweet, footer

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



hide="""
<style>
footer{
	visibility: hidden;
    	position: relative;
}
.viewerBadge_container__1QSob{
    visibility: hidden;
}
.viewerBadge_link__1S137{
    visibility: hidden;
}
#MainMenu{
	visibility: hidden;
}
<style>
"""
st.markdown(hide, unsafe_allow_html=True)



st.markdown("<h1 style='text-align: center'><span style='color: #1DA1F2'>Twitter</span> Thread Extractor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center'>Extracting Twitter threads from Twitter profiles.</p>", unsafe_allow_html=True)

username_url = st.text_input("Enter your Twitter URL", placeholder="https://twitter.com/elonmusk", disabled=False)
st.markdown("""
<details>
<summary><b>You have more than 3200 tweets?</b></summary>
DM me on <a href="https://twitter.com/nainia_ayoub"><i>@nainia_ayoub</i></a> to extract all your threads!
</details>

<style>
    summary:hover{
        color: #1da1f2;
    }
</style>
    
"""
,
unsafe_allow_html=True,)
footer()


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

if username_url:
    username = username_url.split('/')[-1]
    if 'https://twitter.com/' in username_url and username not in 'https://twitter.com/' and " " not in username:
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
        st.error("Enter a valid Twitter URL")