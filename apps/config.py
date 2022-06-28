import configparser
import os.path
import re

import tweepy


class Keys:

    dir = os.getcwd() + "/apps/config.ini"
    config_ini = configparser.ConfigParser()
    config_ini.read(dir, encoding='utf-8')

    CONSUMER_KEY = config_ini.get('CONSUMER_KEY', 'CONSUMER_KEY')
    CONSUMER_SECRET = config_ini.get('CONSUMER_KEY', 'CONSUMER_SECRET')
    ACCESS_TOKEN = config_ini.get('ACCESS_TOKEN', 'ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = config_ini.get('ACCESS_TOKEN', 'ACCESS_TOKEN_SECRET')

class SearchFilter:
    SEARCH_USER = "sekai_in_wonder"
    SEARCH_WORD = ""

def connect_twetter():
    auth = tweepy.OAuthHandler(Keys.CONSUMER_KEY, Keys.CONSUMER_SECRET)
    auth.set_access_token(Keys.ACCESS_TOKEN, Keys.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit = True)
    return api
