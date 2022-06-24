import time

import tweepy

from apps.config import (Keys, SearchFilter, check_user_id,
                         check_user_screen_name, connect_twetter)
from apps.input_file import input_txt, input_user_list

api = connect_twetter()


def get_follower_ids():
    follower_ids = api.get_follower_ids(screen_name="sekai_in_wonder")
    follower_ids_alt = []
    i = 0
    for follower_id in follower_ids:
        i += 1
        if i >= 11:
            break
        print(check_user_screen_name(follower_id))
        print(follower_id)
        follower_ids_alt.append(follower_id)
    return follower_ids_alt
    

def get_user_tweet(user_id):
    user_timeline = api.user_timeline(user_id=user_id)
    '''
    i = 0
    for tweet in user_timeline:
        i += 1
        if i >= 2:
            break
        print('-------------------------------------------')
        print(tweet.id)    
    '''
    return user_timeline[0]

def is_mention(tweet):
    if not tweet.in_reply_to_status_id:
        return True
    else:
        return False

def is_retweet(tweet):
    try:
        if tweet.retweeted_status != "":
            return False
    except AttributeError:
        return True

def is_ng_word(tweet):
    ng_words = ["質問", "募", "集"]
    if tweet.txt in ng_words:
        False
    else:
        True

def favorite_tweet():
    follower_ids = get_follower_ids()
    for user_id in follower_ids:
        tweet = get_user_tweet(user_id)
        print("user:", check_user_screen_name(user_id))
        print("text:", tweet.text)
        print("id:", tweet.id)
        
        if is_mention(tweet) and is_retweet(tweet) and is_ng_word:
            print("fav:True")
            api.create_favorite(tweet.id)
        else:
            print("fav:False")

        print("-"*30)
