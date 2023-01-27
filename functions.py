import streamlit as st
import pandas as pd
import tweepy
import requests

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
        id_replies.append(user_tweet.in_reply_to_status_id)
        ids.append(status_id)
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
            ids.append(status_id)
            id_replies.append(user_tweet.in_reply_to_status_id)
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
    
@st.cache
def extract_threads(df, username):
    df['replied to'] = df['replied to'].fillna(0)
    df['replied to'] = df['replied to'].apply(convert_to_int)
    # potential root tweets in a thread
    df_root_tweets = df[df['replied to'] == 0]
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

@st.cache
def convert_df(df):
  # IMPORTANT: Cache the conversion to prevent computation on every rerun
  return df.to_csv().encode('utf-8')

def theTweet(tweet_url):
	api = "https://publish.twitter.com/oembed?url={}".format(tweet_url)
	response = requests.get(api)
	res = response.json()["html"]
	return res