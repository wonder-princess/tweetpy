import time

import tweepy

from apps.config import Keys, SearchFilter, connect_twetter
from apps.inputcsv import input_user_list

api = connect_twetter()

def output_list():
    list = input_user_list()
    for row in list:
        print(row)

def foo():
    message = "Hello, World!"
    recipient_id = check_user_id("granblue_check")
    api.send_direct_message(recipient_id=recipient_id, text=message)

def check_user_id(screen_name):
    user_id = api.get_user(screen_name=screen_name).id
    return user_id

def send_dm():
    message = "Hello, World!"
    list = input_user_list()
    for user in list:
        recipient_id = check_user_id(user)
        # time.sleep(1)
        api.send_direct_message(recipient_id=recipient_id, text=message)

