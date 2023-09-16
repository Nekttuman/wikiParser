from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

import webbrowser


class Response(QWidget):
    _WIDGET_WIDTH = 500

    def __init__(self, title: str, date: str, snippet: str, link: str):
        super().__init__()

        self._title = QLabel(title)
        self._date = QLabel(date)
        self._snippet = QLabel(snippet)
        self._snippet.setWordWrap(True)
        self._link = link

        self._initUI()

    def _initUI(self):
        ''' Добавляет элементы в layout; стилизует то, что не стилезуется в .qss '''
        self.setFixedWidth(Response._WIDGET_WIDTH)

        layout = QVBoxLayout()
        layout.addWidget(self._title)
        layout.addWidget(self._date)
        layout.addWidget(self._snippet)

        self._title.setProperty("class", "title")
        self._snippet.setWordWrap(True)
        self._title.setWordWrap(True)

        self.setLayout(layout)

    def mousePressEvent(self, event) -> None:
        ''' Открывает ссылки в браузере '''

        if event.button() == Qt.LeftButton:
            webbrowser.open(self._link)


class ResponsesContainerWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def addResponse(self, res: Response):
        ''' Add responses from layout '''

        self.layout.addWidget(res)

    def clear(self):
        ''' Remove responses from layout '''

        if self.layout is not None:
            while self.layout.count():
                item = self.layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
