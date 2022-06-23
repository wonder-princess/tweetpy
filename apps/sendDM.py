import tweepy

from apps.config import Keys, SearchFilter, connect_twetter
from apps.inputcsv import printdata

api = connect_twetter()

def output_list():
    list = printdata()
    for row in list:
        print(row)

def foo():
    message = "Hello, World!"
    recipient_id = check_user_id("granblue_check")
    api.send_direct_message(recipient_id=recipient_id, text=message)

def check_user_id(screen_name):
    user_id = api.get_user(screen_name=screen_name).id
    return user_id
