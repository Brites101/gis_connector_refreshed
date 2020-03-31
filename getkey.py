import requests


# This function returns an access token for EXPA
def get_access_token(token_get_url):
    # Get the access token from an external URL
    access_token = requests.get(token_get_url)

    # Check if we have a valid access token
    if access_token.status_code != 200:
        raise Exception('Unable to get access token', 'ACCESS_TOKEN_INVALID_STATUS', access_token.status_code)

    if len(access_token.text.strip()) != 64:
        raise Exception('Invalid access token ' + access_token.text, 'ACCESS_TOKEN_INVALID_TEXT', access_token.text)

    # Return the access token
    return access_token.text.strip()
