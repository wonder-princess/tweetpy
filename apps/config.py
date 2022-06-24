import tweepy


class Keys:

    CONSUMER_KEY = "d6Z4EUpqAP2oYUHUcPSaoCifN"
    CONSUMER_SECRET = "knReUEAfGGR0fcjmnP491Y6bosp8u75xaI0Oj5ujVmWYcEU5A9"
    ACCESS_TOKEN = "779662566029037568-PhOIFSZdZAdccwkLHeyeTGMhIivVVJY"
    ACCESS_TOKEN_SECRET = "CYXFzppZQhbKg2nujIWTpIwAw3PnuAApYy4sq1geKF2fu"

class SearchFilter:
    SEARCH_USER = "sekai_in_wonder"
    SEARCH_WORD = ""


def connect_twetter():
    auth = tweepy.OAuthHandler(Keys.CONSUMER_KEY, Keys.CONSUMER_SECRET)
    auth.set_access_token(Keys.ACCESS_TOKEN, Keys.ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit = True)
    return api

def check_user_id(screen_name):
    user_id = connect_twetter().get_user(screen_name=screen_name).id
    return user_id

def check_user_screen_name(user_id):
    screen_name = connect_twetter().get_user(user_id=user_id).screen_name
    return screen_name
