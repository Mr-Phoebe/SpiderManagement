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
    if not os.path.exists(file_name):
        csvfile = codecs.open(file_name, 'wb')
        csvfile.write(codecs.BOM_UTF8)
        csvfile.close()
    csvfile = codecs.open(file_name, 'a+', encoding='utf-8')
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(line)


def csv_dic(dic, num, dep, max_len, task_id, file_list):
    file_path = os.path.join(STATIC_ROOT, "data/" + task_id).replace('\\', '/')
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    file_name = file_path + '/csv_' + str(num) + '_' + str(dep) + '.csv'
    file_list.append('csv_' + str(num) + '_' + str(dep) + '.csv')
    if not os.path.exists(file_name):
        csvfile = codecs.open(file_name, 'wb')
        csvfile.write(codecs.BOM_UTF8)
        csvfile.close()
    csvfile = codecs.open(file_name, 'a+', encoding='utf-8')
    field_name = dic.keys()
    writer = csv.DictWriter(csvfile, fieldnames=field_name)
    for i in range(max_len):
        dic_line = {}
        for key, value in dic.items():
            if i >= len(value):
                continue
            dic_line[key] = value[i]
        writer.writerow(dic_line)


def csv_split(fa, num, dep, task_id, file_list):
    line = fa.split('\n')
    for i in line:
        i = i.strip()
        if i != '\n' and i != "":
            csv_line([i], num, dep, task_id, file_list)

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
