import time

from apps.config import (Keys, SearchFilter, check_user_id,
                         check_user_screen_name, connect_twetter)
from apps.fav_tweet import (favorite_tweet, get_follower_ids, get_user_tweet,
                            is_retweet)
from apps.get_timelines import get_home_timelines, get_user_timelines
from apps.input_file import input_img
from apps.post_tweet import is_empty, post_tweet
from apps.send_dm import output_list, send_dm

print("run app")

# foo()
# print("★☆★タイムライン☆★☆")
# get_home_timelines()
# print("★☆★自分のツイート☆★☆")
# get_user_timelines()

# send_dm()

# post_tweet()

# is_empty()

favorite_tweet()

# tweet = get_user_tweet(check_user_id("ebikoring"))
# print(is_retweet(tweet))
