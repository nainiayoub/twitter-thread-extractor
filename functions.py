import streamlit as st
import pandas as pd
import tweepy
import requests
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

def extract_all_tweets(username):
    user_tweets = st.session_state['api'].user_timeline(screen_name=username, 
                            # 200 is the maximum allowed count
                            count = 200,
                            include_rts = False,
                            # Necessary to keep full_text 
                            # otherwise only the first 140 words are extracted
                            tweet_mode = 'extended'
                            )
    user_name = [] 
    user_text_tweet = []
    followers = [] 
    retweets = []
    favs = [] 
    dates = []
    ids = []
    id_replies = []
    for user_tweet in user_tweets:
        status_id = user_tweet.id
        id_replies.append(str(user_tweet.in_reply_to_status_id))
        ids.append(str(status_id))
        # if user_tweet.lang != "fr" and user_tweet.lang != "en":
        dates.append(user_tweet.created_at)
        favs.append(user_tweet.favorite_count)
        user_name.append(user_tweet.user.screen_name)
        user_text_tweet.append(user_tweet.full_text)
        # followers.append(user_tweet.user.followers_count)
        retweets.append(user_tweet.retweet_count)
        

    oldest = status_id - 1
    while len(user_tweets) > 0:
        user_tweets = st.session_state['api'].user_timeline(screen_name=username,count=200,include_rts = False,tweet_mode = 'extended',max_id=oldest)
        
        #save most recent tweets
        for user_tweet in user_tweets:
            status_id = user_tweet.id
            ids.append(str(status_id))
            id_replies.append(str(user_tweet.in_reply_to_status_id))
            dates.append(user_tweet.created_at)
            favs.append(user_tweet.favorite_count)
            user_name.append(user_tweet.user.screen_name)
            user_text_tweet.append(user_tweet.full_text)
            # followers.append(user_tweet.user.followers_count)
            retweets.append(user_tweet.retweet_count)
        
        #update the id of the oldest tweet less one
        oldest = status_id - 1

    # df = pd.DataFrame(list(zip(user_name, ids, user_text_tweet, id_replies, followers, retweeted)), columns=['username', 'status id', 'tweet', 'reply to', 'followers', 'retweeted'])
    df = pd.DataFrame(list(zip(ids, user_name, user_text_tweet, dates, id_replies, favs, retweets)), columns=['status id', 'Username', 'tweet', 'Date', 'replied to', 'Favorites', 'Retweets']) 
    return df

def convert_to_int(num):
    return int(float(num))
    
@st.cache_data
def extract_threads(df, username):
    df['replied to'] = df['replied to'].fillna(0)
    # potential root tweets in a thread
    df_root_tweets = df[df['replied to'] == 'None']
    ids = list(df_root_tweets['status id'])
    threads_url = []
    tweets = []
    dates = []
    favs = []
    rts = []
    for id in ids:
        thread = []
        reply = df.loc[df['replied to'] == id]
        root_tweet = df.loc[df['status id'] == id]
        if not reply.empty:
            # thread.append(list(reply['status id'])[0])
            url = 'https://twitter.com/'+str(username)+'/status/'+str(id)
            tweets.append(list(root_tweet['tweet'])[0])
            dates.append(list(root_tweet['Date'])[0])
            rts.append(list(root_tweet['Retweets'])[0])
            favs.append(list(root_tweet['Favorites'])[0])
            threads_url.append(url)

    df_threads = pd.DataFrame(list(zip(threads_url, tweets, dates, favs, rts)), columns = ['Thread URL', 'Tweet', 'Date', 'Favorites', 'Retweets'])
    return df_threads

@st.cache_data
def convert_df(df):
  # IMPORTANT: Cache the conversion to prevent computation on every rerun
  return df.to_csv().encode('utf-8')

def theTweet(tweet_url):
	api = "https://publish.twitter.com/oembed?url={}".format(tweet_url)
	response = requests.get(api)
	res = response.json()["html"]
	return res


def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style), width=150)


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):

    style = """
    <style>
      MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
     .stApp { bottom: 105px; }
     img{
        background-color: #ddd;
     }
     img:hover{
        background-color: rgba(59,130,246,.5);
     }
    </style>
    """

    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 0, 0, 0),
        width=percent(100),
        color="black",
        text_align="center",
        height="auto",
        opacity=1
    )

    style_hr = styles(
        # display="block",
        # margin=px(8, 8, "auto", "auto"),
        # border_style="inset",
        # border_width=px(2)
    )

    body = p()
    foot = div(
        style=style_div
    )(
        hr(
            style=style_hr
        ),
        body
    )

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


def footer():
    myargs = [
        "Made by ",
        link("https://twitter.com/nainia_ayoub", "@nainia_ayoub"),
        br(),
        link("https://buymeacoffee.com/nainiayoub", image('https://cdn.buymeacoffee.com/assets/img/home-page-v3/bmc-new-logo.png')),
    ]
    layout(*myargs)
