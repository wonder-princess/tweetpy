import time

import tweepy

from apps.config import Keys, SearchFilter, connect_twetter
from apps.input_file import input_txt, input_user_list

api = connect_twetter()

def check_user_id(screen_name):
    user_id = api.get_user(screen_name=screen_name).id
    return user_id

followers_ids = tweepy.Cursor(api.followers_ids, id=check_user_id("sekai_in_wonder"), cursor=-1).items()
for follower_id in followers_ids:
    try:
        user = api.get_user(follower_id)
        user_info = [user.id_str, user.screen_name, user.name, user.created_at]
        print(user_info)
    except tweepy.error.TweepError as e:
        print(e.reason)


