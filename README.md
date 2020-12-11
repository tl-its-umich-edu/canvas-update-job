# Canvas Update Job

The scripts here are intended to be various jobs that might be run against Canvas.

Currently there is just one: `update_accounts.py` and a utility script `util/canvas_oauth` for generating the initial oauth credentials.

To use this script you need two files
`oauth_settings.json`
    This is a manually created file based on this example json.
    This file is created based on creating a Developer API key in Canvas. You need to fill in the information from there.

1. Create Canvas Developer API key
2. Assign the scopes you need
3. Populate the values in this configuration file and save it.
4. redirect_uri can be most things but this example URI is something that will give a response.
5. After you've created this file, run the canvas_oauth.py in util and go through the steps to get canvas_token.json

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

`canvas_token.json`
This is file contains the access and refresh token json from the `util/canvas_oauth.py` script. Use "as-is". An example is like

```json
{"access_token":"1770_lots_of_text","token_type":"Bearer","user":{"id":1,"name":"User Name","global_id":"17700000000000001","effective_locale":"en"},"refresh_token":"1770~_lots_of_text","expires_in":3600}
```
