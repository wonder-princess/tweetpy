import random
import re
import time
from datetime import timedelta
from itertools import count

import tweepy

from apps.checkers import (check_user_id, check_user_screen_name, is_mention,
                           is_ng_word, is_retweet)
from apps.config import connect_twetter
from apps.input_file import input_img, input_txt, input_user_list

api = connect_twetter()

def post_tweet():
    if not input_img():
        api.update_status(status=input_txt())
    else:
        media_ids = []
        i = 0
        for image in input_img():
            i += 1
            if i >= 5:
                break
            img = api.media_upload(image)
            media_ids.append(img.media_id)
        api.update_status(status=input_txt(), media_ids=media_ids) 

def send_dm():
    message = input_txt()
    itr = input_user_list()
    for user in itr:
        recipient_id = check_user_id(user)
        api.send_direct_message(recipient_id=recipient_id, text=message)

def get_follower_ids():
    follower_ids = api.get_follower_ids(screen_name="sekai_in_wonder")
    follower_ids_alt = []
    i = 0
    for follower_id in follower_ids:
        i += 1
        if i >= 6:
            break
        follower_ids_alt.append(follower_id)
    return follower_ids_alt

def favorite_tweet():
    follower_ids = get_follower_ids()
    for user_id in follower_ids:
        tweet = api.user_timeline(user_id=user_id)[0]
        print("user:", check_user_screen_name(user_id))
        print("text:", tweet.text)
        print("id:", tweet.id)
        
        if is_mention(tweet) and is_retweet(tweet) and is_ng_word(tweet):
            print("fav:True")
            # api.create_favorite(tweet.id)
        else:
            print("fav:False")

        print("-"*30)

def ohayou():
    n = random.randint(1,5)
    if n == 1:
        return "おっはー"
    elif n == 2:
        return "aaaaa"
    elif n == 3:
        return "bbbb"
    elif n == 4:
        return "cccc"
    else:
        return "は？きも"

def reply_goodmorning():
    timeline = api.user_timeline(user_id=check_user_id("sekai_princess"))
    # timeline = api.list_timeline(list_id=1527775551108567041, count=5000, include_rts=False)

    goodmorning_tweets = []
    for tweet in timeline:
        if re.match(r'.*おはよう*', tweet.text) and is_mention(tweet) and  is_ng_word(tweet):
            goodmorning_tweets.append(tweet)
    
    for tweet in goodmorning_tweets:
        print("ユーザ名:\n", tweet.user.name)
        print("ツイート本文:\n", tweet.text)
        print("ツイートした時間:\n", tweet.created_at + timedelta(hours=+9))
        print("ツイートID:\n", tweet.id)
        print('*'*30)

        reply_text = "@"+str(tweet.user.screen_name) +"\n"+ ohayou()
        api.update_status(status=reply_text, in_reply_to_status_id = tweet.id)

def test_reply():
    tweet = api.user_timeline(user_id=check_user_id("sekai_princess"))[0]
    reply_text = "@"+str(tweet.user.screen_name) +"\n"+ input_txt()
    api.update_status(status=reply_text, in_reply_to_status_id = tweet.id)
