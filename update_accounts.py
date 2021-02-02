# Update Script for Accounts Discovery URL

import json
import logging

from canvasapi import Canvas
from canvasapi.exceptions import ResourceDoesNotExist, InvalidAccessToken
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

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
        logger.error("Could not refresh access token")
        return ""

def update_discovery_url(api_url: str):
    with open("canvas_token.json") as token_file:
        TOKEN = json.load(token_file)
    with open("oauth_settings.json") as oauth_file:
        OAUTH = json.load(oauth_file)

    access_token = TOKEN.get("access_token")
    try:
        CANVAS = Canvas(api_url, access_token)
        account = CANVAS.get_account(1)
    except InvalidAccessToken:
        logger.info("Access token is invalid, attempting to refresh!")
        access_token = refresh_token(api_url, TOKEN.get("refresh_token"),
                                     OAUTH.get("client_id"), OAUTH.get("client_secret"), OAUTH.get("redirect_uri"))
        CANVAS = Canvas(api_url, access_token)
        account = CANVAS.get_account(1)

        # TODO: Make this URL configurable
        account.update_account_auth_settings(
            sso_settings={"auth_discovery_url": ""})

# TODO: Make this URL configurable
update_discovery_url("https://umich.beta.instructure.com")
update_discovery_url("https://umich.test.instructure.com")
