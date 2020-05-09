from uuid import uuid4

from flask import Flask, request, abort

from definitions import GUI_RESOURCES_DIR
from core import reddit

app = Flask('Retriever for RPAN')
valid_states = []


@app.route('/callback')
def callback():
    error = request.args.get('error', '')
    if error:
        # add some handling here
        print(error)
    state = request.args.get('state', '')
    if not is_valid_state(state):
        abort(403)
    code = request.args.get('code')
    if reddit.get_token(code):
        text = 'Token obtained'
    else:
        text = 'We had trouble obtaining the token'
    html = f'<head>' \
           f'<title>Retriever for RPAN - {text}</title>' \
           f'</head>' \
           f'<body style="font-family:sans-serif;">{text}</body>'
    return html


def create_state() -> str:
    state = str(uuid4())
    save_state(state)
    return state


def is_valid_state(state) -> bool:
    if state in valid_states:
        return True
    return False


def save_state(state):
    valid_states.append(state)
