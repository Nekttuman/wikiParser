from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import *

import json
import logging

from ResponsesWidget import ResponsesContainerWidget, Response
from UrlManager import UrlManager

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'  # Define the format of the timestamp
)


class WikiParser(QMainWindow):
    _WINDOW_SIZE = QSize(600, 400)                      # fixed, px

    def __init__(self):
        super().__init__()

        self._errLabel = QLabel()
        self._exitBtn = QPushButton('×')
        self._minimizeBtn = QPushButton('—')
        self._searchLine = QLineEdit()
        self._searchBtn = QPushButton("Search")

        self._resultsArea = QScrollArea()
        self._responcesContainer = ResponsesContainerWidget()

        self._searchBtn.clicked.connect(self._makeResponce)
        self._exitBtn.clicked.connect(lambda: QApplication.quit())
        self._minimizeBtn.clicked.connect(self.showMinimized)
        self._searchLine.returnPressed.connect(self._makeResponce)

        self._initUI()

    def keyPressEvent(self, event):                     # override
        if event.key() == Qt.Key_Escape:
            logging.info("esc pressed, app quit")
            QApplication.quit()

        # drog n drop window functionality
    def mousePressEvent(self, event):                   # override
        if event.button() == Qt.LeftButton and self.centralWidget().rect().contains(event.pos()):
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):                    # override
        if event.buttons() == Qt.LeftButton and self.dragging:
            new_pos = self.mapToGlobal(event.pos() - self.offset)
            self.move(new_pos)

    def mouseReleaseEvent(self, event):                 # override
        self.dragging = False

    def _initUI(self):
        ''' Добавляет элементы в layout; стилизует то, что не стилезуется в .qss '''

        self.setWindowTitle("WikiFastSearch")
        self.setFixedSize(WikiParser._WINDOW_SIZE)

        self._searchBtn.setProperty("class", "searchBtn")
        self._exitBtn.setProperty("class", "navBtn")
        self._minimizeBtn.setProperty("class", "navBtn")
        self._resultsArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        hlayout1 = QHBoxLayout()
        hlayout1.addWidget(self._errLabel)
        hlayout1.addWidget(self._minimizeBtn)
        hlayout1.addWidget(self._exitBtn)
        self._errLabel.setStyleSheet("color:red;")
        hlayout2 = QHBoxLayout()
        hlayout2.addWidget(self._searchLine)
        hlayout2.addWidget(self._searchBtn)
        vlayout = QVBoxLayout()
        vlayout.setProperty("class", "mainLayout")
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
        ''' отправляет get запрос на wiki, запрос формирует UrlManager '''

        self._responcesContainer.clear()
        self._errLabel.clear()

        if (self._searchLine.text() == ""):
            self._errLabel.setText("Empty request")
            return

        request = QNetworkRequest(
            UrlManager.getSearchRequstUrl(self._searchLine.text()))

        logging.info(f"creating request: \
                {UrlManager.getSearchRequstUrl(self._searchLine.text())}")

        self.nam = QNetworkAccessManager()
        self.nam.finished.connect(self._handleResponse)
        self.nam.get(request)

        # TODO: add connection ckecking
        # if self.nam.networkAccessible != QNetworkAccessManager.Accessible:
        #     self._errLabel.setText("no connection")

    def _handleResponse(self, reply):
        ''' обрабатывает ответ, передает в self._parseJson '''

        if reply.error() == QNetworkReply.NoError:
            data = reply.readAll()
            self._parseJson(data.data())
        else:
            self._errLabel.setText("Sorry, error on our side")
            logging.error("Error: " + reply.errorString())

    def _parseJson(self, data):
        ''' извлекает из данных информацию для _responcesContainer (QWidget) '''

        try:
            parsed_data = json.loads(data)
            logging.info(
                f"response received, wiki json has {len(parsed_data['query']['search'])} items")

            for jsonData in parsed_data['query']['search']:
                self._responcesContainer.addResponse(Response(jsonData['title'],
                                                              jsonData['timestamp'],
                                                              jsonData['snippet'],
                                                              UrlManager.createPageUrl(jsonData['pageid'])))
            if not parsed_data['query']['search']:
                self._errLabel.setText("Sorry, nothing was found")
            else:
                self._resultsArea.setWidget(self._responcesContainer)

        except Exception as e:
            self._errLabel.setText(f"Sorry, error on our side")
            logging.error(f"Error parsing json {e}")
