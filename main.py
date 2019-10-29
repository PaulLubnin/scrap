import argparse
import requests
import re
import os


class LoadHtml:
    """
    Класс загружает требуемую страницу в виде строк
    Делалось на основе gazeta.ru
    """
    def __init__(self, url):
        self.url = url

    def get_html_in_str(self):
        try:
            req = requests.get(self.url)
        except Exception as error:
            print(f'Ошибка:\n'
                  f'{error}')
        else:
            if req.status_code == 200:
                html = req.text
                return html


class LoadNews(LoadHtml):
    """
    Класс обрабатывает загруженные строки при помощи регулярных выражений
    """
    def __init__(self, url=''):
        LoadHtml.__init__(self, url)
        self.html = self.get_html_in_str()

    def get_info(self, expression):
        html = self.html
        pattern = re.compile(expression)
        result = pattern.findall(html)
        return result

    def get_header(self):
        header = self.get_info(r'<meta\sproperty=\"og:title\"\scontent\=(.*)\s/>')
        header = re.sub(r'(\&laquo\;)|(\&raquo\;)', r'"', str(header))
        return header

    def get_subtitle(self):
        subtitle = self.get_info(r'<title>(.*)</title>')
        subtitle = re.sub(r'(\&laquo\;)|(\&raquo\;)', r'"', str(subtitle))
        return subtitle

    def get_text_share(self):
        text_share = self.get_info(r'<meta\sproperty\=\"twitter\:description\"\scontent\=(.*)\s/>')
        text_share = re.sub(r'(\&laquo\;)|(\&raquo\;)', r'"', str(text_share))
        text_share = re.sub(r'(&mdash;)', r'-', str(text_share))
        return text_share

    def get_text_news(self):
        text_news = self.get_info(r'<p>(.*)</p>')
        # регулярки для gazeta.ru
        text_news = re.sub(r'(Н\w{7}:)(.*?)((\w{7}\s\w*\:\s)(\+7\s\(\d{3}\)\s\d{3}'
                           r'\-00\-12))(.*?)(</a>)(\'\,\s\')(<a(.*)(</a>))',
                           r'[\4\5]', str(text_news))
        text_news = re.sub(r'(</p>)(<p>)', '\n\n', str(text_news))
        text_news = re.sub(r"', '", "\n\n", str(text_news))
        text_news = re.sub(r'<[aA]\s{1}href=[\'\"](.*?)[\'\"][^>]*>(.*?)</[aA]>',
                           r'\2 [URL: "\1"]',
                           str(text_news))
        text_news = re.sub(r'(<a\shref\=)(http\:\/\/)(.*)(\starget\s\=\_blank>)(.*)(<\/a>)',
                           r'\5 [URL: "\3"]', str(text_news))
        text_news = re.sub(r'(<a\shref\=)(http\:\/\/ria\.ru)\s(target\=\_blank.)(.*?)(</a>)',
                           r'\4 [URL: "\2"]', str(text_news))
        text_news = re.sub(r'(<b>)(.*?)(</b>)', r'\2', str(text_news))
        text_news = re.sub(r'(&mdash;|&ndash;|&nbsp;)', r'-', str(text_news))
        text_news = re.sub(r'(<span class=\"idea\">)(.*?)(</span>)',
                           r'[ИДЕЯ] \2', str(text_news))
        text_news = re.sub(r'(\&laquo\;)|(\&raquo\;)', r'"', str(text_news))
        # регулярки для lenta.ru
        text_news = re.sub(r'(</p><)((h1)\s(class|id)\=\")topic-title\w*(\s|\"\>)(.*?)(</h1><p>)',
                           r'\n[Заголовок: "\6".] \n', str(text_news))
        text_news = re.sub(r'</p>(<aside class=(\"\w\-\w{6}\-|w{6}\-box)).*(</aside>)<p>',
                           '', str(text_news))
        text_news = re.sub(r'(</p><)((div|aside)\s(class|id)\=\")\w*(\w|\-)\w*(\s|\").*?(<p>)',
                           '', str(text_news))

        text_news = re.sub(r'\\xa0|\\u200b|\\u200b', '', str(text_news))
        text_news = re.sub(r'(</p></div><p\sclass\=\")(\w\-(.*)\"\s)(.*?>)(.*)(</span>)',
                           r'[Автор:\5]', str(text_news))
        # text_news = self.split80_and_write(text_news)
        return text_news

    # если нужен будет словарь
    # def get_news_dict(self):
    #     news_text_dict = {'header': self.get_header(),
    #                       'subtitle': self.get_subtitle(),
    #                       'text_share': self.get_text_share(),
    #                       'text_news': self.get_text_news()}
    #     return news_text_dict

    def merger(self):
        all_info = ''
        all_info += self.get_header() + '\n\n'
        all_info += self.get_subtitle() + '\n\n'
        all_info += self.get_text_share() + '\n\n'
        all_info += self.get_text_news()
        return all_info


class RecordNews:
    """
    Клвсс для записи новостей в файл
    """
    def __init__(self, url):
        self.url = url
        # self.path = re.sub(r'((https)\:\/)(\/www\..*?)(shtml|html)', r'\3txt', str(self.url))
        self.path = re.sub(r'(https\:\/)(\/.*)', r'\2', str(self.url))

    def write(self, news_lines, max_length=80):
        rows = []
        text = news_lines
        while text:
            if len(text) <= max_length:
                rows.append(text)
                text = ''
            else:
                for info in range(max_length + 1, 0, -1):
                    if str.isspace(text[info]):
                        rows.append(text[:info])
                        text = text[info + 1:]
                        break
        try:
            os.makedirs(os.getcwd() + os.path.dirname(self.path))
        except FileExistsError:
            pass
        with open(os.getcwd() + self.path + '.txt', 'a', encoding='utf-8') as file:
            for info in rows:
                file.write(info + '\n')
            print('Новость записана')
        return


def start_program():
    parser = argparse.ArgumentParser()
    parser.add_argument('http', nargs='?')
    return parser


if __name__ == '__main__':
    start = start_program()
    http = start.parse_args()

    if http.http:
        # url = input('Введите URL: \n')
        news = LoadNews(http.http)
        all_info = news.merger()
        rec = RecordNews(http.http)
        rec.write(all_info)
    else:
        print('Неверный адрес')
