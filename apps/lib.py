import re
from datetime import timedelta
from apps.config import connect_twetter
from apps.input_file import Input_file
import sys

class Lib:
    api = connect_twetter()
    input_file = Input_file()

    def get_user_id(self, screen_name):
        user_id = self.api.get_user(screen_name=screen_name).id
        return user_id

    def get_user_screen_name(self, user_id):
        screen_name = self.api.get_user(user_id=user_id).screen_name
        return screen_name

    def get_user_name(self, screen_name):
        user_name = self.api.get_user(screen_name=screen_name).name
        return user_name

    def is_mention(self, tweet):
        if not tweet.in_reply_to_status_id:
            return True
        else:
            return False

    def is_retweet(self, tweet):
        try:
            if tweet.retweeted_status != "":
                return False
        except AttributeError:
            return True

    def is_omit_word(self, tweet):
        omit_words = self.input_file.input_omit_words()
        for omit_word in omit_words:
            if str(omit_word).strip() in tweet.text:
                return False
            else:
                continue
        return True

    def is_omit_user(self, name):
        omit_users = self.input_file.input_omit_user_list()
        for omit_user in omit_users:
            if str(omit_user).strip() == name:
                return False
            else:
                continue
        return True

    def output_log(self, tweet):
        print("user:", tweet.user.name)
        print("id:", tweet.id)
        print("time:", tweet.created_at + timedelta(hours=+9))
        print("text:\n", tweet.text)
        # log = f'user{tweet.user.name}\nid:{tweet.id}\ntime:{tweet.created_at + timedelta(hours=+9)}\n"text:{tweet.text}'
        # print(log)

    def shouldRun(self):
        str = input("よろしい場合は\"y\"を押してください\n")
        if str == "y":
            return True
        else:
            return False

    def create_all_userlist(self, *userlists_ids):
        userlists_ids = userlists_ids[0]
        all_userlist = set()
        userlists = []
        for userlist_ids in userlists_ids:
            userlist = []
            itr = self.api.get_list_members(list_id=userlist_ids, count=500)
            for user in itr:
                userlist.append(user.id)
            userlists.append(set(userlist))
        for userlist in userlists:
            all_userlist = all_userlist.union(userlist)
        all_userlist = list(all_userlist)
        return all_userlist

    def printFuncName(self):
        function_name = sys._getframe().f_code.co_name
        class_name = self.__class__.__name__
        print('{}.{}'.format(function_name, class_name))
