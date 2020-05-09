from PyQt5.QtGui import QFont, QFontDatabase

from definitions import GUI_RESOURCES_DIR


def init():
    QFontDatabase.addApplicationFont(GUI_RESOURCES_DIR + 'fonts/RobotoCondensed-Regular.ttf')


roboto_condensed = 'Roboto Condensed'

title = QFont(roboto_condensed, 36)
subtitle = QFont(roboto_condensed, 26)
button = QFont(roboto_condensed, 12)
line = QFont(roboto_condensed, 12)
