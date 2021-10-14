from tda import auth, client
import json
import secrets

API_KEY_TDA = "	***REMOVED***@AMER.OAUTHAP"
REDIRECT_URI = "http://localhost/"

auth_window = f"https://auth.tdameritrade.com/auth?response_type=code&redirect_uri={REDIRECT_URI}&client_id={API_KEY_TDA}"
auth_website = "https://auth.tdameritrade.com/auth?response_type=code&redirect_uri=http://localhost/&client_id=***REMOVED***@AMER.OAUTHAP"
print(auth_window)