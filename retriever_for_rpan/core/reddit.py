#  Retriever For RPAN - Unofficial streaming utility for the Reddit Public Access Network
#  Copyright (C) 2020 warpspeedchic
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""
This module is meant to handle any requests that should be made to reddit.
"""

import os
import urllib.parse
from typing import Optional

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


def get_video_json():
    """
    Returns a json with the info about the current stream.

    :return: json
    """
    stream_id = os.getenv('STREAM_ID')
    if stream_id is None:
        return None
    _, stream_id = stream_id.split('_')
    response = requests.get(f'https://strapi.reddit.com/videos/t3_{stream_id}', headers=get_headers())
    if response.status_code != 200:
        return None
    return response.json()


def get_live_comments_websocket() -> Optional[str]:
    """
    Returns a websocket URL to live comments of the current stream.

    :return: websocket url
    """
    video_json = get_video_json()
    if video_json is None:
        return None
    live_comments_websocket = video_json['data']['post']['liveCommentsWebsocket']
    return live_comments_websocket


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
        os.environ['STREAM_ID'] = rjson['data']['post']['id']
    return response
