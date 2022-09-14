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

from apps.lib import Lib
from apps.config import UserList, LoginUser, connect_twetter
from apps.input_file import Input_file
# input_img, input_txt, input_sendDM_user_list, input_omit_user_list, input_userlist_list

class Apps:

    api = connect_twetter()
    lib = Lib()
    input_file = Input_file()

    def post_tweet(self):
        if not self.input_file.input_img():
            self.api.update_status(status=self.input_file.input_txt())
        else:
            media_ids = []
            i = 0
            for image in self.input_file.input_img():
                i += 1
                if i >= 5:
                    break
                img = self.api.media_upload(image)
                media_ids.append(img.media_id)
            self.api.update_status(status=self.input_file.input_txt(), media_ids=media_ids)

    def send_dm(self):
        message = self.input_file.input_txt()
        itr = self.input_file.input_sendDM_user_list()
        print("----- 送信ユーザー -----")
        for user in itr:
            
            print(user.strip(), "  ", self.lib.get_user_name(user))
        print("\n", "----- 送信メッセージ -----")
        print(message)
        print("-"*30, "\n")
        if self.lib.shouldRun():
            for user in itr:
                recipient_id = self.lib.get_user_id(user)
                self.api.send_direct_message(recipient_id=recipient_id, text=message)
            print("送信完了しました")
        else:
            print("送信を中断しました")

    def favorite_tweet(self):
        itr = self.api.get_list_members(list_id=UserList.USER_LIST, count=500)
        fav_count = 0
        user_ids = []
        for user in itr:
            user_ids.append(user.id)
        random.shuffle(user_ids)
        for user_id in user_ids:
            tweets = self.api.user_timeline(user_id=user_id, count=10, include_rts=False)
            for tweet in tweets:
                try:
                    self.lib.output_log(tweet)
                    print("***")
                    if self.lib.is_mention(tweet) and self.lib.is_omit_word(tweet) and self.lib.is_retweet(tweet):
                        self.api.create_favorite(tweet.id)
                        fav_count += 1
                        print("【Success : ", str(fav_count).strip(), "】")
                        time.sleep(1)
                        break
                    else:
                        print("Omit tweet")
                        print("【Failure】")
                except Forbidden as e:
                    if e.api_codes == [139]:
                        print(e)
                        print("【Failure】")
                        break
                    else:
                        print(e)
                        print("【Failure】")
                        continue
                except TweepyException as e:
                    print(e)
                    print("【Failure】")
                    continue
                finally:
                    print("-"*30)
            if fav_count >= 50:
                break

    '''
    # 旧バージョン
    # ファボが出来なかった際、過去10ツイートさかのぼってファボ
    def favorite_tweet_old():
        itr = self.api.get_list_members(list_id=UserList.USER_LIST, count=500)
        fav_count = 1
        user_ids = []
        for user in itr:
            user_ids.append(user.id)
        random.shuffle(user_ids)
        for user_id in user_ids:
            if fav_count > 50:
                break
            try:
                tweet = self.api.user_timeline(user_id=user_id, count=1, include_rts=False)[0]
                if is_mention(tweet) and is_ng_word(tweet) and is_retweet(tweet):
                    print("fav:True [", fav_count, "]")
                    output_log(tweet)
                    self.api.create_favorite(tweet.id)
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

    def ohayou(self):
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

    def reply_goodmorning(self):
        itr = self.api.list_timeline(list_id=UserList.USER_LIST, count=5000, include_rts=False)
        goodmorning_tweets = []
        for tweet in itr:
            if re.match(r'.*おはよう*', tweet.text) and self.lib.is_mention(tweet) and  self.lib.is_omit_word(tweet):
                goodmorning_tweets.append(tweet)
        for tweet in goodmorning_tweets:
            self.lib.output_log(tweet)
            print("-"*30)
            reply_text = "@"+str(tweet.user.screen_name) +"\n"+ self.ohayou()
            self.api.update_status(status=reply_text, in_reply_to_status_id = tweet.id)
            time.sleep(1)

    def favorite_resume(self):
        itr = self.api.search_tweets(q="#ポケカ履歴書 -filter:retweets", result_type="recent", count=100)
        fav_count = 0
        for tweet in itr:
            try:
                self.lib.output_log(tweet)
                print("***")
                if self.lib.is_mention(tweet) and self.lib.is_omit_word(tweet) and self.lib.is_omit_user(tweet.user.screen_name):
                    self.api.create_favorite(tweet.id)
                    fav_count += 1
                    print("【Success : ", str(fav_count).strip(), "】")
                    time.sleep(1)
                else:
                    print("Omit tweet")
                    print("【Failure】")
            except Forbidden as e:
                print(e)
                print("【Failure】")
                continue
            except TweepyException as e:
                print(e)
                print("【Failure】")
                continue
            finally:
                print("-"*30)
                if fav_count >= 100:
                    break

    def add_to_list(self):
        all_userlist = self.lib.create_all_userlist(self.input_file.input_userlist_list())
        itr = self.api.get_friend_ids(screen_name=LoginUser.SCREEN_NAME, count=700)
        add_count = 0
        for user_id in itr:
            try:
                print(self.lib.get_user_screen_name(user_id))
                if not user_id in all_userlist:
                    self.api.add_list_member(user_id=user_id, list_id=UserList.USER_LIST)
                    add_count += 1
                    print("【Success : ", str(add_count).strip(), "】")
                    time.sleep(1)
                else:
                    print("Already added")
                    print("【Failure】")
            except TweepyException as e:
                if e.api_codes == [104]:
                    print(e)
                    print("【Failure】")
                    break
                elif e.api_codes == [50]:
                    print("50 - User not found.")
                    print("【Failure】")
                    continue
                elif e.api_codes == [108]:
                    print("108 - Cannot find specified user.")
                    print("【Failure】")
                    continue            
                else:
                    print(self.lib.get_user_screen_name(user_id))
                    print(e)
                    print("【Failure】")
                    continue
            finally:
                print("-"*30)
                if add_count >= 50:
                    break