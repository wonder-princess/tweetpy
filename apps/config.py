import configparser
import os.path

import tweepy

dir = os.getcwd() + "/apps/config.ini"
config_ini = configparser.ConfigParser()
config_ini.read(dir, encoding='utf-8')

class Keys:
    CONSUMER_KEY = config_ini.get('CONSUMER_KEY', 'CONSUMER_KEY')
    CONSUMER_SECRET = config_ini.get('CONSUMER_KEY', 'CONSUMER_SECRET')
    ACCESS_TOKEN = config_ini.get('ACCESS_TOKEN', 'ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = config_ini.get('ACCESS_TOKEN', 'ACCESS_TOKEN_SECRET')

class CallbackURL:
    CALLBACK_URL = config_ini.get('CALLBACK_URL', 'CALLBACK_URL')

class UserList:
    USER_LIST = config_ini.get('USER_LIST', 'USER_LIST')

def connect_twetter():
    auth = tweepy.OAuthHandler(Keys.CONSUMER_KEY, Keys.CONSUMER_SECRET)
    auth.set_access_token(Keys.ACCESS_TOKEN, Keys.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit = True)
    return api
