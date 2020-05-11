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
from PyQt5.QtWidgets import QApplication, QMessageBox

from definitions import DATA_DIR
from core import server
from gui.main import MainWindow
from gui import fonts

if __name__ == "__main__":
    app = QApplication([])
    app.setWindowIcon(QIcon(DATA_DIR + 'img/dog_icon.ico'))

    port_blocker_name = server.get_port_blocker_name()
    if port_blocker_name:
        QMessageBox().warning(None, 'Port already in use!',
                              f'This app requires a specific local port to be open,\n'
                              f'but it seems to be taken by {port_blocker_name}.\n'
                              f"If it's safe to do so, stop the process and try again.")
        sys.exit(-1)

    server_thread = Thread(target=server.run, daemon=True)
    server_thread.start()

    with open(DATA_DIR + 'styles/default.qss') as stylesheet:
        app.setStyleSheet(stylesheet.read())
    fonts.init()
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
