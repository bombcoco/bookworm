import requests
from bs4 import BeautifulSoup
import time
import sys


class Crawl:

    def requestURL(self, data):

        url = data['url']
        custom_hreders = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        r = requests.get(url, headers=custom_hreders)

        data.update({'content': r.content, 'url': url})
        return data

    def getLinks(self, data):

        soup = BeautifulSoup(data['content'], "html.parser")
        soup = soup.find_all('a')
        links = []
        for link in soup:
            if 'http' in link['href']:
                links.append(link['href'])
        data.update({'all': links})
        return data

    def getV2EXTitles(self, data):

        soup = BeautifulSoup(data['content'], "html.parser")
        soup = soup.find_all('span', attrs={'class': 'item_title'})
        titles = []
        for span in soup:
            title = span.text
            href = span.a['href']
            titles.append(title + ' - ' + data['base'] + href)

        data.update({'all': titles})
        return data

    def getBIQUDAOContent(self, data):

        soup = BeautifulSoup(data['content'], "html.parser")
        text = soup.get_text()
        contents = []

        #title = soup.title.get_text()
        #soup = soup.find_all('div', id='chaptercontent')
        #contents = []
        #for s in soup:
        #    content = s.get_text()
        #    contents.append(str(title + '\n' + content))

        contents.append(text)
        data.update({'all': contents})
        return data

    def writeFile(self, data, filename):

        with open(filename, mode='a', encoding='utf-8') as file:
            for a in data['all']:
                file.write(a + '\n')


if __name__ == '__main__':

    crawl = Crawl()
    startPage = 1662108
    for i in range(5):

        print("-", end='')
        sys.stdout.flush()

        i += 1
        startTime = time.time()

        data = {'content': "", 'url': "http://m.biqudao.com/bqge1618/" + str(startPage + i) + ".html" +
                str(i), 'base': 'https://www.v2ex.com', 'all': []}
        d = crawl.requestURL(data)
        # todo
        d = crawl.getBIQUDAOContent(data)

        crawl.writeFile(d, filename='book.txt')

        endTime = time.time()

        if endTime - startTime < 1:
            time.sleep(1)
            print("|", end='')

        sys.stdout.flush()
