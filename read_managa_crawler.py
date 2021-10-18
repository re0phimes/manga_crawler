# -*- ecoding: utf-8 -*-
# @ModuleName: read_managa_crawler
# @Function: 
# @Author: ctx_phi
# @Craete Time: 2021/10/18 16:25

import requests, os
from tqdm import tqdm
from scrapy import Selector
from sys import _getframe

url = "https://www.mangaread.org/manga/nano-machine/chapter-{}/"
manga_name, start_chapter, end_chapter = 'nano_machine', 50, 60

if url == '':
    url = input('please input manga base_url:')
    manga_name, start_chapter, end_chapter = input('please input manga name, start chapter, end chapter:').split()

class MangaCrawler:



    def __init__(self):
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38"
        }
        self.start_chapter = start_chapter
        self.end_chapter = end_chapter
        print('第{}行:'.format(_getframe().f_lineno) + "开始爬取漫画：{}基本信息".format(manga_name))

    def manga_crawler(self, url):
        r = requests.get(url, headers=self.header)
        selector = Selector(text=r.text)
        img_list = selector.xpath("//img[contains(@id, 'image')]/@src").extract()
        img_list = [img.strip() for img in img_list]
        # path
        chapter = url.split('/')[-2]
        if os.path.exists(manga_name + '/' + chapter):
            pass
        else:
            os.mkdir(manga_name + '/' + chapter)
        # download img
        for img in img_list:
            page = img.split('/')[-1]
            print(img)
            r = requests.get(img, headers=self.header)
            with open(manga_name + '/' + chapter + '/' + page, mode='wb') as f:
                f.write(r.content)

    def run_crawler(self):
        failure = []

        for i in tqdm(range(int(self.start_chapter), int(self.end_chapter))):
            try:
                print('starting crawl chapter {}'.format(i))
                self.manga_crawler(url.format(i))
                print('finish')
                print('-' * 100)
            except Exception as e:
                print("line no: {} with error: {}".format(_getframe().f_lineno, e))

                # print(e)

        with open('failure.txt', mode='w', encoding='utf-8') as f:
            f.write(str(failure))

crawler = MangaCrawler()
crawler.run_crawler()
