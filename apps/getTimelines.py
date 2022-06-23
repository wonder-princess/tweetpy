from datetime import timedelta

import tweepy

from apps.config import Keys, SearchFilter, connect_twetter

# import json
# from requests_oauthlib import OAuth1Session

'''
CK = Keys.CONSUMER_KEY
CS = Keys.CONSUMER_SECRET
AT = Keys.ACCESS_TOKEN
ATS = Keys.ACCESS_TOKEN_SECRET

twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理
url = "https://api.twitter.com/1.1/statuses/user_timeline.json" #タイムライン取得エンドポイント
def get_timelines():
    params ={'count' : 5} #取得数
    res = twitter.get(url, params = params)
    if res.status_code == 200: #正常通信出来た場合
        timelines = json.loads(res.text) #レスポンスからタイムラインリストを取得
        for line in timelines: #タイムラインリストをループ処理
            print(line['user']['name']+'::'+line['text'])
            print(line['created_at'])
            print('*'*30)
    else: #正常通信出来なかった場合
        print("Failed: %d" % res.status_code)
'''

api = connect_twetter()

def get_home_timelines():
    
    for status in api.home_timeline(): #タイムラインリストをループ処理
        print("ユーザ名:\n", status.user.name)
        print("ユーザ名:\n", status.id,)
        print("ツイート本文:\n", status.text)
        print("ツイートした時間:\n", status.created_at + timedelta(hours=+9))
        print('*'*30)

def get_user_timelines():

    user = SearchFilter.SEARCH_USER
    
    for status in api.user_timeline(id=user): #タイムラインリストをループ処理
        print("ユーザ名:\n", status.user.name)
        print("ユーザ名:\n", status.id,)
        print("ツイート本文:\n", status.text)
        print("ツイートした時間:\n", status.created_at + timedelta(hours=+9))
        print('*'*30)
