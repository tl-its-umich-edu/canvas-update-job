# Update Script for Accounts Discovery URL

import argparse
import json
import logging
import sys

from canvasapi import Canvas
from canvasapi.exceptions import ResourceDoesNotExist, InvalidAccessToken
from pydantic import BaseModel
import requests

# Set this to DEBUG for more information
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

#Matches up to the oauth_settings.json file
class OAuthSettings(BaseModel):
    account_id: int
    client_id: str
    client_secret: str
    update_discovery_urls: dict[str, str]

# Matches up to the canvas_token.json file
class Token(BaseModel):
    refresh_token: str
    access_token: str
    token_type: str
    expires_in: int
    user: dict

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

def update_discovery_url(canvas_url: str, discovery_url: str, token: Token, settings: OAuthSettings):
    log.info(f"Updating discovery url on {canvas_url} to '{discovery_url}'")
    access_token = token.access_token
    try:
        canvas = Canvas(canvas_url, access_token)
        account = canvas.get_account(1)
    except InvalidAccessToken:
        log.info("Access token is invalid, attempting to refresh!")
        access_token = refresh_token(canvas_url, token.refresh_token,
                                     settings.client_id, settings.client_secret, discovery_url)
        log.debug(access_token)
        canvas = Canvas(canvas_url, access_token)
        account = canvas.get_account(settings.account_id)

    try:
        # TODO: Make this URL configurable
        account.update_account_auth_settings(
            sso_settings={"auth_discovery_url": discovery_url})
    except Exception as e:
        log.error(f"Error updating {api_url} {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Update Canvas Test/Beta Settings')
    parser.add_argument('canvas_token', type=str, help='Canvas Token File')
    parser.add_argument('settings', type=str, help='Settings File')

    args = parser.parse_args()

    try:
        with open(args.canvas_token) as token_file:
            token = Token(**json.load(token_file))
        with open(args.settings) as settings_file:
            oauth = OAuthSettings(**json.load(settings_file))
    except IOError:
        log.exception("Could not read one of the files provided as arguments.")
        sys.exit()

    for canvas_url, discovery_url in oauth.update_discovery_urls.items():
        update_discovery_url(canvas_url, discovery_url, token, oauth)

if __name__ == '__main__':
    main()