# -*- coding: utf-8 -*-
# @Author: HaonanWu
# @Date:   2017-03-15 10:22:40
# @Last Modified by:   HaonanWu
# @Last Modified time: 2017-03-25 12:33:05

import csv
import os
from crawler.tests import *
from SP.settings import STATIC_ROOT


def csv_line(line, num, dep, task_id, file_list):
    file_path = os.path.join(STATIC_ROOT, "data/" + task_id).replace('\\', '/')
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    file_name = file_path + '/csv_' + str(num) + '_' + str(dep) + '.csv'
    file_list.append('csv_' + str(num) + '_' + str(dep) + '.csv')
    csvfile = open(file_name, 'a+', newline='')
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(line)


def csv_brother(ori, num, dep, task_id, file_list):
    cur = ori
    line = []
    while cur:
        try:
            tmp = "" + cur.string
            cur = cur.next_sibling
        except:
            break
        tmp = tmp.strip()
        if tmp != '\n' and tmp != '':
            line.append(tmp.replace('\n', ''))
    if line != []:
        csv_line(line, num, dep, task_id, file_list)


def print_brother(ori, num, dep):
    cur = ori
    line = []
    while cur:
        try:
            tmp = "" + cur.string
            cur = cur.next_sibling
        except:
            break
        tmp.strip()
        if tmp != '\n':
            line.append(tmp.replace('\n', ''))
    if line != []:
        print_temp_line(line, num, dep)

def print_children(ori, num, dep):
    cur = ori
    f1 = codecs.open('test' + str(num) + '_' + str(dep) + '.txt', 'a+', encoding='utf-8')
    try:
        for child in cur.children:
            try:
                tmp = "" + child.string
            except:
                break
            tmp.strip()
            if tmp != '\n':
                f1.write(tmp + "\n" + "dep:  " + str(dep) + "\n")
    except:
        pass
    f1.close()
    pass


def print_tree(now, num, dep, task_id, file_list):
    for child in now.children:
        try:
            child.children  # 有儿子，则继续
            print_tree(child, num, dep + 1, task_id, file_list)
        except Exception as e:
            # print_brother(child, num, dep)
            csv_brother(child, num, dep, task_id, file_list)
