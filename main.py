from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile, QTextStream

import sys

from WikiParser import WikiParser


if __name__ == "__main__":
    app = QApplication(sys.argv)

    stylesheet_file = QFile("styles.qss")
    if stylesheet_file.open(QFile.ReadOnly | QFile.Text):
        stream = QTextStream(stylesheet_file)
        stylesheet = stream.readAll()
        app.setStyleSheet(stylesheet)
        stylesheet_file.close()
    else:
        print('nofile')
    wp = WikiParser()
    wp.show()

    app.exec()
