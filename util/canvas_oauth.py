import json
import requests
import logging
from urllib.parse import urlparse, parse_qs

"""
 Step one, go to Canvas Admin->Developer Keys
 + Developer Key, + API Key

 Fill in Key name, Owner Email
 Redirect URI (as anything, I use https://example.com/oauth_complete)

 Select Enforce Scopes and pick the scopes, add these scopes here.

 After saving get the client_id and key
"""

with open('../oauth_settings.json') as f:
  js = json.load(f)

url_scope = "+".join(js["scopes"])

# Step 1, call this with the client id, redirect_uri configured and scope 
print(f"Go to this URL in a browser and authorize:\n{js['url']}/auth?client_id={js['client_id']}&response_type=code&redirect_uri={js['redirect_uri']}&scope={url_scope}")
auth_response = input('Copy/Paste the full callback URL:')

auth_code = parse_qs(urlparse(auth_response).query).get("code")

"""
oauth2_get = {
        'client_id': js['client_id'],
        'redirect_uri': js'[redirect_uri'],
        'response_type': 'code',
        'scope': url_scope
        }
"""

# print (requests.get(url+"/auth", params=oauth2_get))
# Step 2, Authorize and extract the code. Can this be automated or manual?


# Step 3 POST back to login with code

# This is the code from step 2
oauth2_post = {
    'grant_type': 'authorization_code',
    'client_id': js['client_id'],
    'client_secret': js['client_secret'],
    'redirect_uri': js['redirect_uri'],
    'code': auth_code,
#    'replace_tokens': True
    }

res = (requests.post(js['url']+"/token", data=oauth2_post))
print ("This is your token, place this in a JSON file")
print (res.text)
