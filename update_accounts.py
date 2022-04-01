# Update Script for Accounts Discovery URL

import argparse
import json
import logging
import sys

from canvasapi import Canvas
from canvasapi.exceptions import ResourceDoesNotExist, InvalidAccessToken
import requests

# Set this to DEBUG for more information
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

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

def update_discovery_url(api_url: str, discovery_url: str, token: dict, settings: dict):
    log.info(f"Updating discovery url on {api_url} to '{discovery_url}'")
    access_token = token.get("access_token")
    try:
        canvas = Canvas(api_url, access_token)
        account = canvas.get_account(1)
    except InvalidAccessToken:
        log.info("Access token is invalid, attempting to refresh!")
        access_token = refresh_token(api_url, token.get("refresh_token"),
                                     settings.get("client_id"), settings.get("client_secret"), settings.get("redirect_uri"))
        log.debug(access_token)
        canvas = Canvas(api_url, access_token)
        account = canvas.get_account(1)

    try:
        # TODO: Make this URL configurable
        account.update_account_auth_settings(
            sso_settings={"auth_discovery_url": discovery_url})
    except Exception as e:
        log.error(f"Error updating {api_url} {e.message}")

def main():
    parser = argparse.ArgumentParser(description='Update Canvas Test/Beta Settings')
    parser.add_argument('canvas_token', type=str, help='Canvas Token File')
    parser.add_argument('settings', type=str, help='Settings File')

    args = parser.parse_args()

    try:
        with open(args.canvas_token) as token_file:
            token = json.load(token_file)
        with open(args.settings) as settings_file:
            settings = json.load(settings_file)
    except IOError:
        log.exception("Could not read one of the files provided as arguments.")
        sys.exit()

    for canvas_server, discovery_url  in settings.get("update_discovery_urls", {}).items():
        update_discovery_url(canvas_server, discovery_url, token, settings)

if __name__ == '__main__':
    main()