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

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QComboBox, QLineEdit, QPushButton, QLabel, QWidget, QGridLayout

from definitions import DATA_DIR
from gui import fonts


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
        if self.doggo_pixmap.load(DATA_DIR + 'img/dog.png'):
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
