from PyQt5.QtCore import QUrl, QUrlQuery


class UrlManager:
    _BASE_URL = "https://ru.wikipedia.org/w/"

    @staticmethod
    def createPageUrl(pageid: int) -> str:
        url = QUrl(UrlManager._BASE_URL + "index.php")

        query = QUrlQuery()
        query.addQueryItem('curid', str(pageid))

        url.setQuery(query)
        return url.toString()

    @staticmethod
    def getSearchRequstUrl(userInput: str) -> QUrl:
        url = QUrl(UrlManager._BASE_URL + "api.php")
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
