from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile, QTextStream

import sys
import logging

from WikiParser import WikiParser


if __name__ == "__main__":
    app = QApplication(sys.argv)

    stylesheetFile = QFile("styles.qss")
    if stylesheetFile.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(stylesheetFile)
        stylesheet = stream.readAll()
        app.setStyleSheet(stylesheet)
        stylesheetFile.close()
    else:
        logging.error("stylesheet file read error")
    wp = WikiParser()
    wp.show()

    app.exec()
