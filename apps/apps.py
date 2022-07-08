import random
import re
import time
from datetime import timedelta
import tweepy

from apps.checkers import (check_user_id, check_user_screen_name, is_mention,
                           is_ng_word, is_retweet)
from apps.config import UserList, connect_twetter
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

def favorite_tweet():
    itr = api.get_list_members(list_id=UserList.USER_LIST, count=500)
    fav_count = 0
    user_ids = []
    for user in itr:
        print(user.id)
        user_ids.append(user.id)
    print(user_ids)
    for user_id in user_ids:
        tweet = api.user_timeline(user_id=user_id, count=1, include_rts=False)[0]
        print("user:", tweet.user.name)
        print("text:\n", tweet.text)
        print("time:", tweet.created_at + timedelta(hours=+9))
        print("id:", tweet.id)
        try:
            if is_mention(tweet) and is_ng_word(tweet) and is_retweet(tweet):
                fav_count += 1
                print("fav:True")
                print("count:", fav_count)
                if fav_count > 50:
                    break
                api.create_favorite(tweet.id)
                time.sleep(1)
            else:
                print("fav:False")
        except Exception as e:
                print(e)
                print("fav:False")
                continue
        finally:
            print("-"*30)

def ohayou():
    n = random.randint(1,5)
    if n == 1:
        return "おはようございます！！"
    elif n == 2:
        return "おはようございまっす！"
    elif n == 3:
        return "おはようございますー！"
    elif n == 4:
        return "おはようございますー！！！！"
    else:
        return "おはようございまーーす"

def reply_goodmorning():
    # itr = api.user_timeline(user_id=check_user_id("sekai_princess"))
    itr = api.list_timeline(list_id=UserList.USER_LIST, count=5000, include_rts=False)

    goodmorning_tweets = []
    for tweet in itr:
        if re.match(r'.*おはよう*', tweet.text) and is_mention(tweet) and  is_ng_word(tweet):
            goodmorning_tweets.append(tweet)
    
    for tweet in goodmorning_tweets:
        print("user:", tweet.user.name)
        print("text:\n", tweet.text)
        print("time:", tweet.created_at + timedelta(hours=+9))
        print("id:", tweet.id)
        print("-"*30)

        reply_text = "@"+str(tweet.user.screen_name) +"\n"+ ohayou()
        api.update_status(status=reply_text, in_reply_to_status_id = tweet.id)
        time.sleep(1)

def test_reply():
    tweet = api.user_timeline(user_id=check_user_id("sekai_princess"))[0]
    reply_text = "@"+str(tweet.user.screen_name) +"\n"+ input_txt()
    api.update_status(status=reply_text, in_reply_to_status_id = tweet.id)

def favorite_resume():
    itr = api.search_tweets(q="#ポケカ履歴書", result_type="mixed", count=100)
    fav_count = 0
    for tweet in itr:
        print("user:", tweet.user.name)
        print("text:\n", tweet.text)
        print("time:", tweet.created_at + timedelta(hours=+9))
        print("id:", tweet.id)

        if is_mention(tweet) and is_ng_word(tweet) and is_retweet(tweet):
            fav_count += 1
            print("fav:True")
            print("count:", fav_count)
            try:
                api.create_favorite(tweet.id)
                time.sleep(1)
                if fav_count > 50:
                    break
            except tweepy.TweepErrorn as e:
                print(e)
                print("fav:False")
                continue
            finally:
                print("-"*30)
        else:
            print("fav:False")
