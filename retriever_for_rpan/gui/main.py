import os
import webbrowser

import yaml
from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QGridLayout, QLineEdit, QComboBox, QPushButton, QStackedWidget, QLabel, QVBoxLayout

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

    def __init__(self, text: str):
        super(Button, self).__init__(text)
        self.setFont(fonts.button)


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

        self.layout = QGridLayout()
        self.layout.addWidget(QWidget())
        self.layout.addWidget(self.auth_button, 1, 0, Qt.AlignHCenter)
        self.layout.addWidget(QWidget())
        self.layout.addWidget(QWidget())
        self.setLayout(self.layout)

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.check_for_token)

    def authorize(self):
        self.timer.start()
        webbrowser.open(reddit.get_authorization_url())

    def check_for_token(self):
        if 'ACCESS_TOKEN' in os.environ:
            self.token_found.emit()
            self.timer.stop()


class StreamSetupWidget(QWidget):

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

        self.layout = QGridLayout()
        self.layout.setSpacing(6)
        self.layout.addWidget(self.username_line, 1, 0, 1, 2)
        self.layout.addWidget(self.stream_title_line, 2, 0, 1, 2)
        self.layout.addWidget(self.subreddit_combo, 3, 0, 1, 2)
        self.layout.addWidget(self.start_stream_button, 4, 0, 1, 2)
        self.layout.addWidget(QWidget(), 5, 0, 1, 2)
        self.setLayout(self.layout)

    def set_username(self):
        self.username_line.setText(f'u/{reddit.get_username()}')


class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.title_widget = TitleWidget()

        self.auth_widget = AuthWidget()
        self.auth_widget.token_found.connect(self.on_token_found)
        self.stream_setup_widget = StreamSetupWidget()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(self.auth_widget)
        self.stacked_widget.addWidget(self.stream_setup_widget)
        # self.stacked_widget.setCurrentIndex(1)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title_widget, alignment=Qt.AlignHCenter)
        self.layout.addWidget(self.stacked_widget)
        self.setLayout(self.layout)

        self.setWindowTitle('Retriever for RPAN')
        self.setFixedSize(480, 320)
        self.setContentsMargins(50, 0, 50, 0)

    def on_token_found(self):
        self.stream_setup_widget.set_username()
        self.stacked_widget.setCurrentIndex(1)
