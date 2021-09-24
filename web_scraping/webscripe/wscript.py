from urllib.request import urlopen
from bs4 import BeautifulSoup

url_aj = 'https://www.aljazeera.com'
filepath = 'html/aj.html'


class NewsScraper:
    __url = ''
    __data = ''
    __wlog = None
    __soup = None
    def __init__(self, url, wlog):
        self.__url = url
        self.__wlog = wlog
    
    def retrive_webpage(self):
        try:
            html = urlopen(self.__url)
        except Exception as e:
            print(e)
            self.__wlog.report(e)
        else:
            self.__data = html.read()
            if len(self.__data) > 0:
                print("Retrive Successfully")
    def write_webpage_as_html(self, filepath=filepath, data=''):
        try:
            with open(filepath, 'wb') as fobj:
                if data:
                    fobj.write(data)
                else:
                    fobj.write(self.__data)
        except Exception as e:
            print(e)
            self.__wlog.report(e)

    def read_webpage_from_html(self, filepath=filepath):
        try:
            with open(filepath) as fobj:
                self.__data = fobj.read()
        except Exception as e:
            print(e)
            self.__wlog.report(e)

    def change_url(self, url):
        self.__url = url
    
    def print_data(self):
        print(self.__data)
    
    def convert_data_to_bs4(self):
        self.__soup = BeautifulSoup(self.__data, "html.parser")
    
    def parse_soup_to_simple_html(self):
        news_list = self.__soup.find_all(['h1', 'h2', 'h3', 'h4', 'span'])
        
        htmltext = '''
        <html>
            <head>
                <title> News link </title>
            </head>
            <body>
                {NEWS_LINKS}
            </body>
        </html>
        '''

        news_links = '<ol>'
        for tag in news_list:
            if tag.parent.get('href'):
                link = self.__url  + tag.parent.get('href')
                title = tag.string
                news_links += f"<li><a href='{link}' target='_blank'>{title}</a></li>"
        news_links += '</ol>'
        htmltext = htmltext.format(NEWS_LINKS=news_links)
        self.write_webpage_as_html(filepath='html/news_link.html', data=htmltext.encode())