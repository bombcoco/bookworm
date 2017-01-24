#!/usr/bin/which python3
# -*- coding: utf-8 -*-
import time
import sys
import re
import os

import requests
from bs4 import BeautifulSoup


class Crawler:

    def requestURL(self, data):

        url = data['url']
        custom_headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'identity',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'
        }
        r = requests.get(url, headers=custom_headers)

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
            titles.append(title + ' - https://www.v2ex.com' + href)

        data.update({'all': titles})
        return data

    def getBIQUDAOContent(self, data):

        soup = BeautifulSoup(data['content'], "html.parser")
        text = soup.get_text()
        contents = []

        title = soup.title.get_text()
        soup = soup.find('div', id='chaptercontent')
        content = soup.get_text()
        stripped_content = self.find_between(content, '点此举报』', '『加入书签')
        contents.append(str(title + '\n' + stripped_content))

        data.update({'all': contents})
        return data

    # https://stackoverflow.com/questions/3368969/find-string-between-two-substrings
    def find_between(self, s, first, last):

        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]

    def writeFile(self, data, filename):

        with open(filename, mode='a', encoding='utf-8') as file:
            for a in data['all']:
                file.write(a + '\n')


if __name__ == '__main__':

    crawler = Crawler()

    startPage = 1662170
    for i in range(500):

        print("-", end='')
        sys.stdout.flush()

        startTime = time.time()

        data = {'content': "", 'url': "http://m.biqudao.com/bqge1618/" +
                str(startPage + i) + ".html", 'all': []}

        d = crawler.requestURL(data)
        d = crawler.getBIQUDAOContent(d)

        crawler.writeFile(d, filename='book.txt')

        endTime = time.time()
        intervalTime = endTime - startTime

        if intervalTime < 1:
            time.sleep(intervalTime)
            print("|", end='')

        sys.stdout.flush()
