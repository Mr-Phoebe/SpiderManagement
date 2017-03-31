# -*- coding: utf-8 -*-
# @Author: HaonanWu
# @Date:   2017-03-15 10:22:04
# @Last Modified by:   HaonanWu
# @Last Modified time: 2017-03-15 11:06:01

from crawler.Node import *

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


def get_pos(now, contain, string):
    try:
        for child in now.children:
            get_pos(child, contain, string)
    except Exception as e:
        try:
            tmp = "" + now.string
            if check_substring(tmp.strip(), string):
                contain.append(Node(now))
        except:
            pass
        return


'''
def get_pos(now, contain, string):
    try:
        for child in now.children:
            get_pos(child, contain, string)
    except AttributeError as e:
        try:
            tmp = "" + now.string
            if check_substring(tmp.strip(), string):
                contain.append(Node(now))
        except:
            pass
        return
'''
