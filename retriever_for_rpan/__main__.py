import sys
from threading import Thread

from PyQt5.QtWidgets import QApplication

from definitions import GUI_RESOURCES_DIR
from core import server
from gui.main import MainWindow
from gui import fonts

if __name__ == "__main__":
    server_thread = Thread(target=server.run, daemon=True)
    server_thread.start()

    app = QApplication([])
    app.setStyle('fusion')
    with open(GUI_RESOURCES_DIR + 'styles/default.qss') as stylesheet:
        app.setStyleSheet(stylesheet.read())
    fonts.init()
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
