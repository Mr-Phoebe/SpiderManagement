# -*- coding: utf-8 -*-
# @Author: HaonanWu
# @Date:   2017-03-15 10:23:15
# @Last Modified by:   HaonanWu
# @Last Modified time: 2017-03-18 10:31:24

from bs4 import BeautifulSoup
import requests
from crawler.dfs_tree import *
from crawler.print_tree import *
from crawler.get_unique import *
from crawler.tests import *


def get_bs4(url):
    # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    headers = {'User-Agent': user_agent}
    r = requests.get(url, headers=headers)
    return BeautifulSoup(r.text, "html.parser")


def get_all_fit(bs, now, num, task_id):
    li = filter(lambda x: x.attrs['class'] == now[1], bs.findAll(now[0], {'class': now[1]}))
    for item in li:
        print_tree(item, num, 0, task_id)

def crawler(id, url, string):
    # url = 'http://interbrand.com/best-brands/best-global-brands/2016/ranking/'
    # string = '178,119 $m'
    file_path = "data\\"
    if not os.path.exists(file_path):
        os.mkdir(file_path)

    contain = []
    soup_packetpage = get_bs4(url)
    if contain == []:
        return False
    get_pos(soup_packetpage, contain, string)

    fa_list = keep_unique(map(get_parent, contain))

    num = 0
    for fa in fa_list:
        num += 1
        get_all_fit(soup_packetpage, fa, num, id)
    return True
