# -*- ecoding: utf-8 -*-
# @ModuleName: test
# @Function: 
# @Author: ctx_phi
# @Craete Time: 2021/10/22 9:20

# -*- ecoding: utf-8 -*-
# @ModuleName: read_managa_crawler
# @Function:
# @Author: ctx_phi
# @Craete Time: 2021/10/18 16:25

import requests, os
from tqdm import tqdm
from scrapy import Selector
from sys import _getframe

# url = "https://www.mangaread.org/manga/nano-machine/chapter-{}/"
url = "https://www.mangaread.org/manga/solo-leveling-manhwa/"



class MangaCrawler:

    def __init__(self, url):
        self.header = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Edg/94.0.992.38"
        }
        self.start_chapter = 0
        self.end_chapter = 0
        self.base_url = url + "chapter-{}/"
        self.web_newest_chapter = 0
        self.downloaded_chapter = 0

        # 获取网站上最新chapter
        r = requests.get(url, headers=self.header)
        selector = Selector(text=r.text)
        newest_chapter_list = selector.xpath('//ul/li[contains(@class,"manga-chapter")]/a/@href').extract()
        self.web_newest_chapter = int(newest_chapter_list[0].split('/')[-2].replace('chapter-', '')) if len(
            newest_chapter_list) > 0 else None
        # print('web newest chapter is {}'.format(self.web_newest_chapter))

        # 检查已下载的量
        self.manga_name = url.split('/')[-2].replace('-', '_')
        if os.path.exists('data/' + self.manga_name):
            downloaded_list = os.listdir('data/' + self.manga_name)
            downloaded_list = [int(chapter_name.replace('chapter-', '')) for chapter_name in downloaded_list]
            self.downloaded_chapter = int(max(downloaded_list)) if len(downloaded_list) > 0 else 0
            # print('previous downloaded last chapter is {}'.format(self.downloaded_chapter))
        else:
            os.mkdir('data/' + self.manga_name)

        # 判断如何下载
        if self.web_newest_chapter == self.downloaded_chapter:
            print('【{}】没有更新，仍在{}章'.format(self.manga_name, self.web_newest_chapter))
            print('退出程序......')
            # exit()
        if self.downloaded_chapter == 0:
            self.start_chapter = 0
            self.end_chapter = self.web_newest_chapter
            print('本地未下载：{}, 全新下载从{} - {}章'.format(self.manga_name, self.start_chapter, self.end_chapter))
        if (self.web_newest_chapter > self.downloaded_chapter) and (self.downloaded_chapter > 0):
            self.start_chapter = self.downloaded_chapter
            self.end_chapter = self.web_newest_chapter
            print('本地已经有漫画{}:1-{}章，现在开始下载{}-{}'.format(self.manga_name, self.start_chapter, int(self.start_chapter) + 1, self.end_chapter))


    def manga_crawler(self, url):
        r = requests.get(url, headers=self.header)
        selector = Selector(text=r.text)
        img_list = selector.xpath("//img[contains(@id, 'image')]/@src").extract()
        img_list = [img.strip() for img in img_list]
        # path
        chapter = url.split('/')[-2]
        if os.path.exists('data/' + self.manga_name + '/' + chapter):
            pass
        else:
            os.mkdir('data/' + self.manga_name + '/' + chapter)
        # download img
        for img in img_list:
            page = img.split('/')[-1]
            print(img)
            r = requests.get(img, headers=self.header)
            with open('data/' + self.manga_name + '/' + chapter + '/' + page, mode='wb') as f:
                f.write(r.content)

    def run_crawler(self):
        failure = []

        for i in tqdm(range(int(self.start_chapter), int(self.end_chapter))):
            try:
                print('starting crawl chapter {}'.format(i))
                self.manga_crawler(self.base_url.format(i))
                print('finish')
                print('-' * 100)
            except Exception as e:
                print("line no: {} with error: {}".format(_getframe().f_lineno, e))

                # print(e)

        with open('failure.txt', mode='w', encoding='utf-8') as f:
            f.write(str(failure))

crawler = MangaCrawler(url)
crawler.run_crawler()
