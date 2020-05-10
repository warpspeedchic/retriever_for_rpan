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

import sys
from threading import Thread

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

from definitions import DATA_DIR
from core import server
from gui.main import MainWindow
from gui import fonts

if __name__ == "__main__":
    server_thread = Thread(target=server.run, daemon=True)
    server_thread.start()

    app = QApplication([])
    with open(DATA_DIR + 'styles/default.qss') as stylesheet:
        app.setStyleSheet(stylesheet.read())
    app.setWindowIcon(QIcon(DATA_DIR + 'img/dog_icon.ico'))
    fonts.init()
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
