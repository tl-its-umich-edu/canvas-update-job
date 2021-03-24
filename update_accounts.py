# Update Script for Accounts Discovery URL

import argparse
import json
import logging
import os

from canvasapi import Canvas
from canvasapi.exceptions import ResourceDoesNotExist, InvalidAccessToken
import requests

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def refresh_token(api_url: str, refresh_token: str, client_id: str, client_secret: str, redirect_uri: str) -> str:
    access_token = requests.post(api_url+"/login/oauth2/token",
                                 data=[("grant_type", "refresh_token"),
                                       ("refresh_token", refresh_token),
                                       ("client_id", client_id),
                                       ("client_secret", client_secret),
                                       ("redirect_uri", redirect_uri)
                                       ],
                                 )

    # Check for error, and return the token if no error
    if access_token.status_code == requests.codes.ok:
        return access_token.json().get("access_token")
    else:
        log.error("Could not refresh access token")
        return ""

def update_discovery_url(api_url: str, discovery_url: str):
    with open(args.canvas_token) as token_file:
        TOKEN = json.load(token_file)
    with open(args.oauth_settings) as oauth_file:
        OAUTH = json.load(oauth_file)

    access_token = TOKEN.get("access_token")
    try:
        CANVAS = Canvas(api_url, access_token)
        account = CANVAS.get_account(1)
    except InvalidAccessToken:
        log.info("Access token is invalid, attempting to refresh!")
        access_token = refresh_token(api_url, TOKEN.get("refresh_token"),
                                     OAUTH.get("client_id"), OAUTH.get("client_secret"), OAUTH.get("redirect_uri"))
        CANVAS = Canvas(api_url, access_token)
        account = CANVAS.get_account(1)

        # TODO: Make this URL configurable
        account.update_account_auth_settings(
            sso_settings={"auth_discovery_url": discovery_url})

parser = argparse.ArgumentParser(description='Update Canvas Test/Beta Settings')
parser.add_argument('canvas_token', type=str, help='Canvas Token File')
parser.add_argument('oauth_settings', type=str, help='OAuth Settings File')

args = parser.parse_args()

if not os.path.isfile(args.canvas_token):
    log.warn("Canvas Token file does not exist, must provide the path to this file")
    sys.exit()
if not os.path.isfile(args.oauth_settings):
    log.warn("OAuth Settings file does not exist, must provide the path to this file")
    sys.exit()

# TODO: Make this URL configurable?
update_discovery_url("https://umich.beta.instructure.com", "")
update_discovery_url("https://umich.test.instructure.com", "https://canvas-dev.dsc.umich.edu/")


