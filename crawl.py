import requests
from bs4 import BeautifulSoup

class Crawl:

    def requestURL(self, data):
        url = data['url']
        r = requests.get(url)

        data.update({'content': r.content, 'url': url})
        return data

    def getLinks(self, data):
        soup = BeautifulSoup(data['content'], "html.parser")
        soup = soup.findAll('a')
        links = []
        for link in soup:
            if 'http' in link['href']:
                links.append(link['href'])
        data.update({'all_links': links})
        return data


def main():

    crawl = Crawl()
    data = {'content': "",'url': "https://wiredcraft.com", 'all_links': []}
    d = crawl.requestURL(data)
    d = crawl.getLinks(d)
    print(d['all_links'])
    print(len(d['all_links']))

main()
