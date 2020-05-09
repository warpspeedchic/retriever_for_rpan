"""
This module is meant to handle any requests that should be made to reddit.
"""

import os
import urllib.parse

import requests
import requests.auth
import yaml

from definitions import CONFIG_DIR
from core import flaskapp

with open(CONFIG_DIR) as stream:
    config = yaml.safe_load(stream)


def get_headers() -> dict:
    """
    Constructs a dictionary of request headers and returns it.

    :return: headers
    """
    headers = {'User-agent': config['user_agent']}

    access_token = os.getenv('ACCESS_TOKEN')
    if access_token:
        headers['Authorization'] = 'Bearer ' + access_token

    return headers


def get_me():
    """
    Returns json data containing information about the currently authorized user.

    :return: json
    """
    headers = get_headers()
    response = requests.get('http://oauth.reddit.com/api/v1/me', headers=headers)
    return response.json()


def get_username() -> str:
    """
    Returns the username of the currently authorized user.

    :return: username
    """
    me = get_me()
    return me['name']


def get_authorization_url() -> str:
    """
    Returns a code authorization URL.

    :return: URL
    """
    state = flaskapp.create_state()
    params = {'client_id': config['client_id'],
              'response_type': 'code',
              'state': state,
              'redirect_uri': config['redirect_uri'],
              'scope': '*'}
    url = 'https://www.reddit.com/api/v1/authorize?' + urllib.parse.urlencode(params)
    return url


def get_token(code: str) -> bool:
    """
    Gets an access token using the code flow.
    Saves it in an env var called 'ACCESS_TOKEN' and returns True.
    Returns False if it fails.

    :param code: code received from reddit's callback
    :return: bool
    """
    client_auth = requests.auth.HTTPBasicAuth(config['client_id'], '')
    post_data = {'grant_type': 'authorization_code',
                 'code': code,
                 'redirect_uri': config['redirect_uri']}
    headers = {'User-agent': config['user_agent']}
    response = requests.post('https://ssl.reddit.com/api/v1/access_token',
                             auth=client_auth,
                             data=post_data,
                             headers=headers)
    token_json = response.json()
    try:
        os.environ['ACCESS_TOKEN'] = token_json['access_token']
        return True
    except KeyError:
        return False


def post_broadcast(title: str, subreddit: str) -> requests.Response:
    """
    Posts a broadcast request to a specified subreddit.

    :param title: Title of the broadcast
    :param subreddit: Subreddit to which the broadcast should be posted
    :return: requests.Response
    """
    headers = get_headers()
    title = urllib.parse.quote(title)
    url = f'https://strapi.reddit.com/r/{subreddit}/broadcasts?title={title}'
    response = requests.post(url, data={}, headers=headers)
    if response.status_code == 200:
        rjson = response.json()
        os.environ['STREAMER_KEY'] = rjson['data']['streamer_key']
        os.environ['STREAM_URL'] = rjson['data']['post']['url']
    return response
