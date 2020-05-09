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
This module defines a Flask app which should be ran on localhost to interpret reddit's callbacks.
"""

from uuid import uuid4

from flask import Flask, request, abort

from core import reddit

app = Flask('Retriever for RPAN')
valid_states = []


@app.route('/callback')
def callback():
    """
    Handles callbacks from reddit. Retrieves an auth code and passes it to reddit.get_token()

    :return: html
    """
    error = request.args.get('error', '')
    if error:
        # add some handling here
        print(error)
    state = request.args.get('state', '')
    if not is_valid_state(state):
        abort(403)
    code = request.args.get('code')
    if reddit.get_token(code):
        text = 'Token obtained, you may now close this tab'
    else:
        text = 'We had trouble obtaining the token'
    html = f'<head>' \
           f'<title>Retriever for RPAN - {text}</title>' \
           f'</head>' \
           f'<body style="font-family:sans-serif;">{text}</body>'
    return html


def create_state() -> str:
    """
    Creates a state string and stores it in a list to make callbacks verifiable.

    :return: uuid4 string
    """
    state = str(uuid4())
    save_state(state)
    return state


def is_valid_state(state: str) -> bool:
    """
    Checks if state has been created by the app.

    :param state: uuid4 string
    :return: True if state is valid
    """
    if state in valid_states:
        return True
    return False


def save_state(state: str):
    """
    Appends the list of valid states.

    :param state: uuid4 string
    """
    valid_states.append(state)
