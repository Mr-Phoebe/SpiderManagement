# -*- coding: utf-8 -*-
# @Author: HaonanWu
# @Date:   2017-03-15 10:22:04
# @Last Modified by:   HaonanWu
# @Last Modified time: 2017-04-01 22:46:29

from crawler.Node import *
from crawler.print_tree import *

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
        contain.append(now)
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
    if method:
        for item in li:
            print_tree(item, num, 0, task_id, file_list)
