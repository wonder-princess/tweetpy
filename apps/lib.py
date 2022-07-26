import re
from datetime import timedelta
from apps.config import connect_twetter
from apps.input_file import input_omit_user_list, input_omit_words

api = connect_twetter()

def get_user_id(screen_name):
    user_id = api.get_user(screen_name=screen_name).id
    return user_id

def get_user_screen_name(user_id):
    screen_name = api.get_user(user_id=user_id).screen_name
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

def is_omit_word(tweet):
    omit_words = input_omit_words()
    for omit_word in omit_words:
        if str(omit_word).strip() in tweet.text:
            return False
        else:
            continue
    return True

def is_omit_user(name):
    omit_users = input_omit_user_list()
    for omit_user in omit_users:
        if str(omit_user).strip() == name:
            return False
        else:
            continue
    return True

def output_log(tweet):
    print("user:", tweet.user.name)
    print("id:", tweet.id)
    print("time:", tweet.created_at + timedelta(hours=+9))
    print("text:\n", tweet.text)

def shouldRun():
    str = input("よろしい場合は\"y\"を押してください\n")
    if str == "y":
        return True
    else:
        return False

def create_all_userlist(*userlists_ids):
    userlists_ids = userlists_ids[0]
    all_userlist = set()
    userlists = []
    for userlist_ids in userlists_ids:
        userlist = []
        itr = api.get_list_members(list_id=userlist_ids, count=500)
        for user in itr:
            userlist.append(user.id)
        userlists.append(set(userlist))
    for userlist in userlists:
        all_userlist = all_userlist.union(userlist)
    all_userlist = list(all_userlist)
    # for i, str in enumerate(all_userlist):
    #     print(str)
    #     all_userlist[i] = str[1:-1]
    return all_userlist
