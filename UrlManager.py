from PyQt5.QtCore import QUrl, QUrlQuery

class UrlManager:
    _baseUrl = "https://ru.wikipedia.org/w/"

    @staticmethod
    def createPageUrl(pageid: int) -> str:
        url = QUrl(UrlManager._baseUrl + "index.php")

        query = QUrlQuery()
        query.addQueryItem('curid', str(pageid))

        url.setQuery(query)
        return url.toString()

    @staticmethod
    def getSearchResponceUrl(userInput: str) -> QUrl:
        url = QUrl(UrlManager._baseUrl + "api.php")
        search = str(QUrl.toPercentEncoding(userInput), 'utf-8')
        params = {'action': 'query',
                  'list': 'search',
                  'utf8': '',
                  'format': 'json',
                  'srsearch': search
                  }
        query = QUrlQuery()
        for key, value in params.items():
            query.addQueryItem(key, value)
        url.setQuery(query)
        return url