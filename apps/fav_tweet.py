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
        if i >= 4:
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

def favorite_tweet():
    follower_ids = get_follower_ids()
    for user_id in follower_ids:
        tweet = get_user_tweet(user_id)
        print("user:", check_user_screen_name(user_id))
        print("text:", tweet.text)
        print("id:", tweet.id)

        api.create_favorite(tweet.id)
