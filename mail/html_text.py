from html.parser import HTMLParser
from re import sub


class HTMLParser_pp(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def de_html(text):
    parser = HTMLParser_pp()
    parser.feed(text)
    parser.close()
    return parser.text()


if __name__ == '__main__':
    test_text = '<html><body><b>Project:</b> DeHTML<br><b>Description:</b><br>test</body></html>'
    print(de_html(test_text))
