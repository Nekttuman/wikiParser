from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QSize,Qt
from PyQt5.QtGui import *

import json

from ResponsesWidget import ResponsesContainerWidget, Response
from UrlManager import UrlManager


class WikiParser(QMainWindow):
    def __init__(self):
        super().__init__()

        self._errLabel = QLabel()
        self._exitBtn = QPushButton('×')
        self._minimizeBtn = QPushButton('—')
        self._searchLine = QLineEdit()
        self._searchLine.setFocus()
        self._searchBtn = QPushButton("Search")

        self._resultsArea = QScrollArea()
        

        self._srw = ResponsesContainerWidget()

        self._searchBtn.clicked.connect(self._makeResponce)
        self._exitBtn.clicked.connect(lambda: QApplication.quit())
        self._minimizeBtn.clicked.connect(self.showMinimized)
        self._searchLine.returnPressed.connect(self._makeResponce)

        self._initUI()

    def _initUI(self):
        self.setWindowTitle("WikiFastSearch")
        self.setFixedSize(600, 400)

        self._resultsArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self._resultsArea.setFrameShape(QScrollArea.NoFrame)
        self._exitBtn.setFixedSize(QSize(35,35))
        self._exitBtn.setStyleSheet("background-color:#121212;font-size:24px; border:none;")
        self._minimizeBtn.setFixedSize(QSize(35,35))
        self._minimizeBtn.setStyleSheet("background-color:#121212;font-size:16px; border:none;")
        self.setStyleSheet("font-size:14px")

        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(self._errLabel)
        hlayout1.addWidget(self._minimizeBtn)
        hlayout1.addWidget(self._exitBtn)
        self._errLabel.setStyleSheet("color:red;")
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(self._searchLine)
        hlayout2.addWidget(self._searchBtn)
        vlayout = QVBoxLayout()
        vlayout.addLayout(hlayout2)
        vlayout.addWidget(self._resultsArea)
        vlayout.addLayout(hlayout1)
        vlayout.setDirection(QVBoxLayout.BottomToTop)
        vlayout.setSpacing(20)
        vlayout.setContentsMargins(20, 10, 20, 20)

        widget = QWidget()
        widget.setLayout(vlayout)
        self.setCentralWidget(widget)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)


    def _makeResponce(self):
        self._srw.clear()
        self._errLabel.clear()
        if (self._searchLine.text() == ""):
            self._errLabel.setText("Empty responce")

        request = QNetworkRequest(
            UrlManager.getSearchResponceUrl(self._searchLine.text()))

        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self._handleResponse)
        self.nam.get(request)

    def _handleResponse(self, reply):
        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            self._parseJson(data.data())
        else:
            self._errLabel.setText("Error: " + reply.errorString())

    def _parseJson(self, data):
        try:
            parsed_data = json.loads(data)
            for response in parsed_data['query']['search']:
                self._srw.addResult(Response(response['title'],
                                                 response['timestamp'],
                                                 response['snippet'],
                                                 UrlManager.createPageUrl(response['pageid'])))
            if not parsed_data['query']['search']:
                self._errLabel.setText("Sorry, nothing was found")
            else:
                self._resultsArea.setWidget(self._srw)

        except Exception as e:
            self._errLabel.setText(f"Error parsing JSON: {e}")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.quit()

# drog n drop window functionality
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.centralWidget().rect().contains(event.pos()):
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.dragging:
            new_pos = self.mapToGlobal(event.pos() - self.offset)
            self.move(new_pos)

    def mouseReleaseEvent(self, event):
        self.dragging = False

