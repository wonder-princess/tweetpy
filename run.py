from webbrowser import get

from apps.getTimelines import get_home_timelines, get_user_timelines
from apps.send_dm import check_user_id, foo, output_list, send_dm

print("hello")

# output_list()

print(check_user_id("WhatMakesTheSky"))
print(check_user_id("granblue_check"))

# foo()
# print("★☆★タイムライン☆★☆")
# get_home_timelines()
# print("★☆★自分のツイート☆★☆")
# get_user_timelines()

send_dm()
