import requests
from bs4 import BeautifulSoup
import time


class Crawl:

    def requestURL(self, data):

        url = data['url']
        r = requests.get(url)

        data.update({'content': r.content, 'url': url})
        return data

    def getLinks(self, data):

        soup = BeautifulSoup(data['content'], "html.parser")
        soup = soup.find_all('a')
        links = []
        for link in soup:
            if 'http' in link['href']:
                links.append(link['href'])
        data.update({'all_links': links})
        return data

    def getTitles(self, data):

        soup = BeautifulSoup(data['content'], "html.parser")
        soup = soup.find_all('span', attrs={'class': 'item_title'})
        titles = []
        for span in soup:
            title = span.text.strip()
            href = span.a['href']
            titles.append(title + ' - ' + data['base'] + href)

        data.update({'all_titles': titles})
        return data

    def writeFile(self, data, filename):

        with open(filename, mode='a', encoding='utf-8') as file:
            for title in data['all_titles']:
                file.write(title + '\n')


if __name__ == '__main__':

    crawl = Crawl()
    for i in range(50):

        print("-", end='')
        i += 1
        startTime = time.time()

        data = {'content': "", 'url': "https://www.v2ex.com/go/programmer?p=" +
                str(i), 'base': 'https://www.v2ex.com', 'all_links': [], 'all_titles': []}
        d = crawl.requestURL(data)
        d = crawl.getTitles(d)

        crawl.writeFile(d, filename='book.txt')

        endTime = time.time()

        if endTime - startTime < 1:
            time.sleep(1)
            print("|", end='')
