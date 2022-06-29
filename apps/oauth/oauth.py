from requests_oauthlib import OAuth1Session

API_KEY = "d6Z4EUpqAP2oYUHUcPSaoCifN"
API_KEY_SECRET = "knReUEAfGGR0fcjmnP491Y6bosp8u75xaI0Oj5ujVmWYcEU5A9"

callback_url = "https://twitter.com/sekai_in_wonder"
request_endpoint_url = "https://api.twitter.com/oauth/request_token"
authenticate_url = "https://api.twitter.com/oauth/authenticate"

session_req = OAuth1Session(API_KEY, API_KEY_SECRET)
response_req = session_req.post(request_endpoint_url, params={"oauth_callback": callback_url})
response_req_text = response_req.text

oauth_token_kvstr = response_req_text.split("&")

print(oauth_token_kvstr)

token_dict = {x.split("=")[0]: x.split("=")[1] for x in oauth_token_kvstr}
oauth_token = token_dict["oauth_token"]

print("認証URL:", f"{authenticate_url}?oauth_token={oauth_token}")

oauth_verifier = input("OAuth Verifierを入力してください> ")

access_endpoint_url = "https://api.twitter.com/oauth/access_token"

session_acc = OAuth1Session(API_KEY, API_KEY_SECRET, oauth_token, oauth_verifier)
response_acc = session_acc.post(access_endpoint_url, params={"oauth_verifier": oauth_verifier})
response_acc_text = response_acc.text

access_token_kvstr = response_acc_text.split("&")
acc_token_dict = {x.split("=")[0]: x.split("=")[1] for x in access_token_kvstr}
access_token = acc_token_dict["oauth_token"]
access_token_secret = acc_token_dict["oauth_token_secret"]

print("Access Token       :", access_token)
print("Access Token Secret:", access_token_secret)
print("User ID            :", acc_token_dict["user_id"])
print("Screen Name        :", acc_token_dict["screen_name"])
