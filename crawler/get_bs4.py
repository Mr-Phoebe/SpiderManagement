# -*- coding: utf-8 -*-
# @Author: HaonanWu
# @Date:   2017-03-15 10:23:15
# @Last Modified by:   HaonanWu
# @Last Modified time: 2017-04-12 15:36:36

from bs4 import BeautifulSoup
import requests
from crawler.dfs_tree import *
from crawler.print_tree import *
from crawler.get_function import *
from crawler.tests import *


def get_bs4(url):
    # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
    try:
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        headers = {'User-Agent': user_agent}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")
        [script.extract() for script in soup.findAll('script')]
        [style.extract() for style in soup.findAll('style')]
        return soup
    except Exception as e:
        print e
        return None



def crawler(id, url, string, method):
    # url = 'http://interbrand.com/best-brands/best-global-brands/2016/ranking/'
    # string = '178,119 $m'
    file_path = os.path.join(STATIC_ROOT, "data\\").replace('\\', '/')
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    if os.path.exists(file_path + id):
        shutil.rmtree(file_path + id)
    string = string.strip()

    anchor = []
    soup_packetpage = get_bs4(url)
    
    if soup_packetpage == None:
        return []

    get_anchor_pos(soup_packetpage, anchor, string)

    if anchor == []:
        return []

    fa_list = []
    for node in anchor:
        fa_list.append(node.get_father())
    anchor = keep_unique(fa_list, anchor)

    file_list = []
    num = 0
    for node in anchor:
        num += 1
        get_all_fit_path(soup_packetpage, node, num, id, file_list, method)
    ############ 简洁抓取
    # 先得到对于每一个fa_list，得到它关于findAll的所有元素的LCA，找出最多的那个LCA，复杂度为O(N^2)
    # 解析LCA
    # 按照路径以及最终的attrs['class']分类
    # 将record中的内容按照标签路径（将路径变成json，然后进行hash）进行分类


    # need to change it , make zip while clicking download
    # make_zip(file_path, id)
    return list(set(file_list))
