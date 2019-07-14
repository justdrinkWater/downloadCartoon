# coding:utf-8

import os
import re

import bs4
import execjs
import fake_useragent
import requests


class DownloadPage:
    def get_content(self, url):
        ua = fake_useragent.UserAgent()
        headers = {
            'User_Agent': ua.random}
        response = requests.get(url, headers=headers)
        r = response.text
        a = r.encode('ISO-8859-1').decode(requests.utils.get_encodings_from_content(r)[0])
        return a

    def get_page_chapter(self, url, dir_path):
        content = self.get_content(url)
        sel = bs4.BeautifulSoup(content, 'lxml')
        div = bs4.BeautifulSoup(str(sel.select_one('.max-h200')), 'lxml')
        for li in div.find_all("li"):
            a_url = li.find("a")
            if a_url:
                url = a_url.get("href")
                self.download_chapter('http://www.pufei.net' + url, a_url.get_text(), dir_path)

    def get_js(self):
        f = open("base64decode.js", 'r', encoding='utf-8')
        line = f.readline()
        html_str = ''
        while line:
            html_str = html_str + line
            line = f.readline()
        return html_str

    def base_64_decode(self, data):
        js_str = self.get_js()
        ctx = execjs.compile(js_str)
        return ctx.call('f', data)

    def get_image(self, img_urls):
        response = requests.get(img_urls)
        if response.status_code == 200:
            return response.content

    def download_chapter(self, url, chapter_name, dir_path):
        content = self.get_content(url)
        search_obj = re.findall(r'packed="(.+)";eval', content, re.S)
        count = 1
        for url2 in self.base_64_decode(search_obj[0]):
            if isinstance(url2, str):
                if url2:
                    image_path = dir_path + '/' + chapter_name + '/P-%s.jpg' % count
                    if not os.path.exists(dir_path + '/' + chapter_name):
                        os.makedirs(dir_path + '/' + chapter_name)
                    if not os.path.exists(image_path):
                        image = self.get_image("http://res.img.pufei.net/" + url2)
                        if image:
                            with open(image_path, 'wb') as f:
                                f.write(image)
                                count += 1
