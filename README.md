# Canvas Update Job

The scripts here are intended to be various jobs that might be run against Canvas.

Currently there is just one: `update_accounts.py` and a utility script `util/canvas_oauth` for generating the initial oauth credentials.

To use this script you need two files 
* `oauth_settings.json` 
    This is a manually created file based on this example json.
    This file is created based on creating a Developer API key in Canvas. You need to fill in the information from there. This script needs two scopes to run. Other scripts may need different scopes.
    * url:PUT|/api/v1/accounts/:account_id/sso_settings 
    * url:GET|/api/v1/accounts/:id

```json
    {
    "client_id": "client_id #",
    "client_secret": "client secret",
    "url": "https://umich.instructure.com/login/oauth2",
    "redirect_uri": "https://example.com/oauth_complete",
    "scopes": ["url:PUT|/api/v1/accounts/:account_id/sso_settings", 
          "url:GET|/api/v1/accounts/:id"
        ]
    }
```

1. Create Canvas Developer API key. Because this is intended to be run only on test you can check "Test Cluster Only". This needs to be run in **production** first and you'll need to wait a few weeks for it to populate to test/beta.
1. Assign the scopes you need
1. The url probably needs to be production, if you set this up in test/beta it will be erased on the next refresh. 
1. Populate the values in this configuration file and save it.
1. redirect_uri can be most things but this example URI is something that will give a response.
1. After you've created this file, run the canvas_oauth.py in util and go through the steps to get canvas_token.json

* `canvas_token.json`
This is file contains the access and refresh token json from the `util/canvas_oauth.py` script. Use "as-is".  You'll want to run this against production Canvas first, then it will also be available in test/beta.

An example is like:

```json
{"access_token":"1770_lots_of_text","token_type":"Bearer","user":{"id":1,"name":"User Name","global_id":"17700000000000001","effective_locale":"en"},"refresh_token":"1770~_lots_of_text","expires_in":3600}
```
