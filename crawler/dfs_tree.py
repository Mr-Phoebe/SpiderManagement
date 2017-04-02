# -*- coding: utf-8 -*-
# @Author: HaonanWu
# @Date:   2017-03-15 10:22:04
# @Last Modified by:   HaonanWu
# @Last Modified time: 2017-04-02 13:10:24

from crawler.Node import *
from crawler.print_tree import *
from crawler.tests import *
import json

def check_substring(stra, strb):
    lista = list(stra)
    listb = list(strb)
    j = 0
    l = len(listb)
    for i in lista:
        if listb[j] == i:
            j += 1
            if j == l:
                return True
    return False


# get LCA of nodeX and nodeY, O(dep)
def LCA(nodex, nodey):
    xdep = nodex.get_dep()
    ydep = nodey.get_dep()
    if xdep > ydep:
        nodex, nodey = nodey, nodex
    dist = ydep - xdep
    xdomNode = nodex.bs4node
    ydomNode = nodey.bs4node
    while dist != 0:
        ydomNode = ydomNode.parent
        dist -= 1
    while xdomNode != ydomNode:
        xdomNode = xdomNode.parent
        ydomNode = ydomNode.parent
    return Node(xdomNode)

# get the anchors position
def get_anchor_pos(now, contain, string):
    try:
        for child in now.children:
            get_anchor_pos(child, contain, string)
    except Exception as e:
        try:
            tmp = "" + now.string
            if check_substring(tmp.strip(), string):
                contain.append(Node(now))
        except:
            pass
        return


# get all the Node with the same CSS
def get_all_fit_css(bs, now, num, task_id, file_list):
    li = filter(lambda x: x.attrs['class'] == now[1], bs.findAll(now[0], {'class': now[1]}))
    for item in li:
        print_tree(item, num, 0, task_id, file_list)


# get all the Node with the same Path and CSS
def get_pos_path(now, contain, path, node, lastclass):
    if 'class' in now.attrs:
        lastclass = now.attrs['class']
    if path == node.path and lastclass == node.get_father()[1]:
        contain.append(Node(now))
        return
    try:
        for child in now.children:
            if child.name != None:
                path.append(child.name)
                get_pos_path(child, contain, path, node, lastclass)
                path.pop()
    except:
        pass
    return


# get all the Node with the same Path and CSS
def get_all_fit_path(bs, node, num, task_id, file_list, method):
    li = []
    get_pos_path(bs, li, [], node, [])
    cnt = 0
    if method == 'true':  # 简洁抓取
        for item in li:
            print_tree(item.bs4node, num, 0, task_id, file_list)
    else:  # 非简洁抓取
        cnt_node = {}
        cnt_max = -1
        node_max = None
        for item in li:
            if cnt > 4:
                break
            lcanode = LCA(item, node)
            nodejson = json.dumps((lcanode.get_path(), lcanode.get_father()))
            if nodejson in cnt_node:
                cnt_node[nodejson] += 1
            else:
                cnt_node[nodejson] = 1
            if cnt_node[nodejson] > cnt_max:
                cnt_max = cnt_node[nodejson]
                node_max = lcanode
            cnt += 1
        print(cnt)
        csv_split(node_max.bs4node.get_text(), 1, 0, task_id, file_list)
        # 法1：这样输出一种
        # 法2：传入一个bs4node，然后按照(path, father)来分类
