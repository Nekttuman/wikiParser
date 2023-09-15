from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import webbrowser


class Response(QWidget):
    def __init__(self, title: str, date: str, snippet: str, link: str):
        super().__init__()

        self._title = QLabel(title)
        self._date = QLabel(date)
        self._snippet = QLabel(snippet)
        self._snippet.setWordWrap(True)
        self._link = link

        self.initUI()

        self.setFixedWidth(500)

    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(self._title)
        layout.addWidget(self._date)
        layout.addWidget(self._snippet)

        self._title.setStyleSheet("font-size:14px")
        self._snippet.setWordWrap(True)
        self._title.setWordWrap(True)

        self.setLayout(layout)

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            webbrowser.open(self._link)


class ResponsesContainerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def addResult(self, res: Response):
        self.layout.addWidget(res)

    def clear(self):
        if self.layout is not None:
            while self.layout.count():
                item = self.layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
