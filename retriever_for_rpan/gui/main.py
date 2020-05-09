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

import os
import webbrowser

import pyperclip as pyperclip
import yaml
from PyQt5.QtCore import QTimer, pyqtSignal, Qt, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QComboBox, QPushButton, QStackedWidget, QLabel, \
    QVBoxLayout, QMessageBox

from definitions import CONFIG_DIR, GUI_RESOURCES_DIR
from core import reddit
from gui import fonts

with open(CONFIG_DIR) as stream:
    config = yaml.safe_load(stream)


class ComboBox(QComboBox):

    def __init__(self):
        super(ComboBox, self).__init__()
        self.setFont(fonts.line)


class LineEdit(QLineEdit):

    def __init__(self):
        super(LineEdit, self).__init__()
        self.setFont(fonts.line)


class Button(QPushButton):

    def __init__(self, text: str = None):
        super(Button, self).__init__(text)
        self.setFont(fonts.button)
        self.setMinimumWidth(80)


class TitleWidget(QWidget):

    def __init__(self):
        super(TitleWidget, self).__init__()

        self.doggo_label = QLabel()
        self.doggo_label.setAlignment(Qt.AlignLeft)
        self.doggo_label.setFixedSize(60, 100)

        self.doggo_pixmap = QPixmap()
        if self.doggo_pixmap.load(GUI_RESOURCES_DIR + 'img/dog.png'):
            self.doggo_pixmap = self.doggo_pixmap.scaled(self.doggo_label.size(), Qt.KeepAspectRatio,
                                                         transformMode=Qt.SmoothTransformation)
            self.doggo_label.setPixmap(self.doggo_pixmap)

        self.title = QLabel('Retriever')
        self.title.setFont(fonts.title)

        self.subtitle = QLabel('for RPAN')
        self.subtitle.setFont(fonts.subtitle)
        self.subtitle.setAlignment(Qt.AlignHCenter)

        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        self.layout.addWidget(self.doggo_label, 0, 0, 2, 1)
        self.layout.addWidget(self.title, 0, 1)
        self.layout.addWidget(self.subtitle, 1, 1)
        self.setLayout(self.layout)


class AuthWidget(QWidget):

    token_found = pyqtSignal()

    def __init__(self):
        super(AuthWidget, self).__init__()

        self.auth_button = Button('Authorize')
        self.auth_button.clicked.connect(self.authorize)

        self.help_button = Button('Help')
        self.help_button.clicked.connect(self.help)

        self.layout = QGridLayout()
        self.layout.addWidget(QWidget())
        self.layout.addWidget(self.auth_button, 1, 0, Qt.AlignHCenter)
        self.layout.addWidget(self.help_button, 2, 0, Qt.AlignHCenter)
        self.layout.addWidget(QWidget())
        self.layout.addWidget(QWidget())
        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.check_for_token)

    @staticmethod
    def help():
        help_url = 'https://github.com/warpspeedchic/Retriever-for-RPAN/blob/master/README.md'
        webbrowser.open(help_url)

    def authorize(self):
        self.timer.start()
        webbrowser.open(reddit.get_authorization_url())

    def check_for_token(self):
        if 'ACCESS_TOKEN' in os.environ:
            self.token_found.emit()
            self.timer.stop()


class StreamSetupWidget(QWidget):

    stream_started = pyqtSignal()

    def __init__(self):
        super(StreamSetupWidget, self).__init__()

        self.username_line = LineEdit()
        self.username_line.setPlaceholderText('Username')
        self.username_line.setReadOnly(True)

        self.stream_title_line = LineEdit()
        self.stream_title_line.setPlaceholderText('Stream title')

        self.subreddit_combo = ComboBox()
        for subreddit in config['subreddits']:
            self.subreddit_combo.addItem(f'r/{subreddit}')

        self.start_stream_button = Button('Start streaming')
        self.start_stream_button.clicked.connect(self.start_stream)

        self.disable_all_widgets()

        self.layout = QGridLayout()
        self.layout.setSpacing(6)
        self.layout.addWidget(self.username_line, 1, 0, 1, 2)
        self.layout.addWidget(self.stream_title_line, 2, 0, 1, 2)
        self.layout.addWidget(self.subreddit_combo, 3, 0, 1, 2)
        self.layout.addWidget(self.start_stream_button, 4, 0, 1, 2)
        self.layout.addWidget(QWidget(), 5, 0, 1, 2)
        self.setLayout(self.layout)

    def initialize(self):
        self.username_line.setText(f'u/{reddit.get_username()}')
        self.enable_all_widgets()

    def start_stream(self):
        self.disable_all_widgets()

        title = self.stream_title_line.text()
        if len(title) == 0:
            QMessageBox().information(self, 'Insufficient title length', 'Your title must be longer.')
            self.enable_all_widgets()
            return

        _, subreddit = self.subreddit_combo.currentText().split('/')

        response = reddit.post_broadcast(title, subreddit)
        status_code = response.status_code
        if status_code != 200:
            if subreddit == 'pan' and status_code == 503:
                error_str = "r/pan is unavailable right now.\nTry a different subreddit."
            else:
                error_str = f"Couldn't start a stream, status code: {status_code}"
            QMessageBox().information(self, 'Stream setup unsuccessful', error_str)
            self.enable_all_widgets()
            return

        self.stream_started.emit()

    def disable_all_widgets(self):
        self.username_line.setDisabled(True)
        self.stream_title_line.setDisabled(True)
        self.subreddit_combo.setDisabled(True)
        self.start_stream_button.setDisabled(True)

    def enable_all_widgets(self):
        self.username_line.setEnabled(True)
        self.stream_title_line.setEnabled(True)
        self.subreddit_combo.setEnabled(True)
        self.start_stream_button.setEnabled(True)


class StreamReadyWidget(QWidget):

    def __init__(self):
        super(StreamReadyWidget, self).__init__()

        self.key_line = LineEdit()
        self.key_line.setPlaceholderText('Streamer key')
        self.key_line.setReadOnly(True)
        self.copy_key_button = Button('Copy stream key')
        self.copy_key_button.clicked.connect(self.copy_key)

        self.rtmp_line = LineEdit()
        self.rtmp_line.setPlaceholderText('RTMP URL')
        self.rtmp_line.setReadOnly(True)
        self.copy_rtmp_button = Button('Copy server URL')
        self.copy_rtmp_button.clicked.connect(self.copy_rtmp)

        self.open_stream_url_button = Button('Open stream URL')
        self.open_stream_url_button.clicked.connect(self.open_stream_url)

        self.layout = QGridLayout()
        self.layout.addWidget(QWidget())
        self.layout.addWidget(self.key_line, 1, 0, 1, 4)
        self.layout.addWidget(self.rtmp_line, 2, 0, 1, 4)
        self.layout.addWidget(self.copy_key_button, 1, 4, 1, 1)
        self.layout.addWidget(self.copy_rtmp_button, 2, 4, 1, 1)
        self.layout.addWidget(self.open_stream_url_button, 3, 0, 1, 5)
        self.layout.addWidget(QWidget())
        self.setLayout(self.layout)

    def initialize(self):
        self.key_line.setText(os.getenv('STREAMER_KEY'))
        self.rtmp_line.setText('rtmp://ingest.redd.it/inbound/')

    def copy_key(self):
        pyperclip.copy(self.key_line.text())

    def copy_rtmp(self):
        pyperclip.copy(self.rtmp_line.text())

    @staticmethod
    def open_stream_url():
        if 'STREAM_URL' not in os.environ:
            return
        webbrowser.open(os.getenv('STREAM_URL'))


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.title_widget = TitleWidget()

        self.auth_widget = AuthWidget()
        self.auth_widget.token_found.connect(self.on_token_found)
        self.stream_setup_widget = StreamSetupWidget()
        self.stream_setup_widget.stream_started.connect(self.on_stream_started)
        self.stream_ready_widget = StreamReadyWidget()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.auth_widget)
        self.stacked_widget.addWidget(self.stream_setup_widget)
        self.stacked_widget.addWidget(self.stream_ready_widget)
        self.stacked_widget.setCurrentIndex(0)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title_widget, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)

        self.setWindowTitle('Retriever for RPAN')
        self.setFixedSize(450, 320)

    @pyqtSlot()
    def on_token_found(self):
        self.stream_setup_widget.initialize()
        self.stacked_widget.setCurrentIndex(1)

    @pyqtSlot()
    def on_stream_started(self):
        self.stream_ready_widget.initialize()
        self.stacked_widget.setCurrentIndex(2)
