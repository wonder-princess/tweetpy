import re

from apps.config import connect_twetter


def check_user_id(screen_name):
    user_id = connect_twetter().get_user(screen_name=screen_name).id
    return user_id

def check_user_screen_name(user_id):
    screen_name = connect_twetter().get_user(user_id=user_id).screen_name
    return screen_name

def is_mention(tweet):
    if not tweet.in_reply_to_status_id:
        return True
    else:
        return False

def is_retweet(tweet):
    try:
        if tweet.retweeted_status != "":
            return False
    except AttributeError:
        return True

def is_ng_word(tweet):
    if re.match(r'.*質問|募|集.*', tweet.text):
        return False
    else:
        return True
