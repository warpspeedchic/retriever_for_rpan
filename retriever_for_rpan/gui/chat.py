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

import json

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtWebSockets import QWebSocket
from PyQt5.QtWidgets import QWidget, QGridLayout

from core import reddit
from gui.widgets import PlainTextEdit


class Chat(QObject):

    comment_received = pyqtSignal(str)

    def __init__(self):
        super(Chat, self).__init__()
        self.websocket = QWebSocket()
        self.websocket.textMessageReceived.connect(self.on_text_message_received)

    def connect(self):
        live_comments_websocket = reddit.get_live_comments_websocket()
        if live_comments_websocket is None:
            return
        self.websocket.open(QUrl(live_comments_websocket))

    @pyqtSlot(str)
    def on_text_message_received(self, response):
        self.comment_received.emit(response)


class ChatWidget(QWidget):

    def __init__(self):
        super(ChatWidget, self).__init__()
        self.setWindowTitle('Chat')
        self.chat = Chat()
        self.chat.comment_received.connect(self.on_comment_received)
        self.chat.connect()

        self.message_area = PlainTextEdit()
        self.message_area.setReadOnly(True)

        self.layout = QGridLayout()
        self.layout.addWidget(self.message_area)
        self.setLayout(self.layout)

    @pyqtSlot(str)
    def on_comment_received(self, comment):
        comment = json.loads(comment)
        payload = comment['payload']
        author = payload['author']
        body = payload['body']
        self.message_area.appendHtml(f'<b>{author}</b>: {body}')
