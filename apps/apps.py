from itertools import count
import random
import re
import time
import tweepy
from tweepy.errors import (
    BadRequest, Forbidden, HTTPException, NotFound, TooManyRequests,
    TweepyException, TwitterServerError, Unauthorized
)
from datetime import timedelta

from apps.lib import (check_user_id, check_user_screen_name, is_mention,
                           is_omit_word, is_retweet, output_log, shouldRun, is_omit_user, create_all_userlist)
from apps.config import UserList, LoginUser, connect_twetter
from apps.input_file import input_img, input_txt, input_sendDM_user_list, input_omit_user_list, input_userlist_list

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
    itr = input_sendDM_user_list()
    print("----- 送信ユーザー -----")
    for user in itr:
        print(user, end='')
    print("----- 送信メッセージ -----")
    print(message)
    print("-"*30, "\n")
    if shouldRun():
        for user in itr:
            recipient_id = check_user_id(user)
            api.send_direct_message(recipient_id=recipient_id, text=message)
        print("送信完了しました")
    else:
        print("送信を中断しました")

def favorite_tweet():
    itr = api.get_list_members(list_id=UserList.USER_LIST, count=500)
    fav_count = 0
    user_ids = []
    for user in itr:
        user_ids.append(user.id)
    random.shuffle(user_ids)
    for user_id in user_ids:
        tweets = api.user_timeline(user_id=user_id, count=10, include_rts=False)
        for tweet in tweets:
            if is_mention(tweet) and is_omit_word(tweet) and is_retweet(tweet):
                try:
                    api.create_favorite(tweet.id)
                    fav_count += 1
                    print("Success [", fav_count, "]")
                    output_log(tweet)
                    time.sleep(1)
                    break
                except Forbidden as e:
                    if e.api_codes == [139]:
                        print("Failure")
                        print(e)
                        output_log(tweet)
                        break
                    else:
                        print("Failure")
                        print(e)
                        output_log(tweet)
                        continue
                except TweepyException as e:
                    print("Failure")
                    print(e)
                    output_log(tweet)
                    continue
                finally:
                    print("-"*30)
            else:
                print("fav:False")
                output_log(tweet)
                print("-"*30)
        if fav_count >= 50:
            break

'''
# 旧バージョン
# ファボが出来なかった際、過去10ツイートさかのぼってファボ
def favorite_tweet_old():
    itr = api.get_list_members(list_id=UserList.USER_LIST, count=500)
    fav_count = 1
    user_ids = []
    for user in itr:
        user_ids.append(user.id)
    random.shuffle(user_ids)
    for user_id in user_ids:
        if fav_count > 50:
            break
        try:
            tweet = api.user_timeline(user_id=user_id, count=1, include_rts=False)[0]
            if is_mention(tweet) and is_ng_word(tweet) and is_retweet(tweet):
                print("fav:True [", fav_count, "]")
                output_log(tweet)
                api.create_favorite(tweet.id)
                fav_count += 1
                time.sleep(1)
            else:
                print("fav:False")
                output_log(tweet)
        except Exception as e:
                print("fav:False")
                print(e)
                output_log(tweet)
                continue
        finally:
            print("-"*30)             
'''

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
    itr = api.list_timeline(list_id=UserList.USER_LIST, count=5000, include_rts=False)
    goodmorning_tweets = []
    for tweet in itr:
        if re.match(r'.*おはよう*', tweet.text) and is_mention(tweet) and  is_omit_word(tweet):
            goodmorning_tweets.append(tweet)
    for tweet in goodmorning_tweets:
        output_log(tweet)
        print("-"*30)
        reply_text = "@"+str(tweet.user.screen_name) +"\n"+ ohayou()
        api.update_status(status=reply_text, in_reply_to_status_id = tweet.id)
        time.sleep(1)

def favorite_resume():
    itr = api.search_tweets(q="#ポケカ履歴書 -filter:retweets", result_type="recent", count=100)
    fav_count = 0
    for tweet in itr:
        try:
            if is_mention(tweet) and is_omit_word(tweet) and is_omit_user(tweet.user.screen_name):
                api.create_favorite(tweet.id)
                fav_count += 1
                print("Success [", fav_count, "]")
                output_log(tweet)
                time.sleep(1)
            else:
                print("fav:False")
                output_log(tweet)
        except Forbidden as e:
            if e.api_codes == [139]:
                print("Failure")
                print(e)
                output_log(tweet)
                break
            else:
                print("Failure")
                print(e)
                output_log(tweet)
                continue
        except TweepyException as e:
            print("Failure")
            print(e)
            output_log(tweet)
            continue
        finally:
            print("-"*30)
        if fav_count >= 100:
            break

def test_add_to_list():
    all_userlist = create_all_userlist(input_userlist_list())
    itr = api.get_friend_ids(screen_name=LoginUser.SCREEN_NAME, count=200)
    add_count = 0
    for user_id in itr:
        if not user_id in all_userlist:
            try:
                print("-"*30)
                api.add_list_member(user_id=user_id, list_id=UserList.USER_LIST)
                add_count += 1
                print("Success [", add_count, "]")
                print(check_user_screen_name(user_id))
                time.sleep(1)
            except TweepyException as e:
                if e.api_codes == [104]:
                    print("Failure")
                    print(check_user_screen_name(user_id))
                    print(e)
                    break
                else:
                    print("Failure")
                    print(check_user_screen_name(user_id))
                    print(e)
                    continue
        else:
            print("-"*30)
            print("Failure")
            print(check_user_screen_name(user_id))
            print("Already added")
        if add_count >= 50:
            break