# -*- coding: utf-8 -*-
# @Author: HaonanWu
# @Date:   2017-03-18 10:34:37
# @Last Modified by:   HaonanWu
# @Last Modified time: 2017-03-18 10:34:44

import json, zipfile, os, shutil


def keep_unique(li, anchor):
    fa_set = set()
    result = []
    for i in range(len(li)):
        if json.dumps(li[i]) not in fa_set:
            result.append(anchor[i])
            fa_set.add(json.dumps(li[i]))
    return result

def make_zip(file_path, id):
    zip_name = file_path + 'zip' + str(id) + '.zip'
    if os.path.exists(zip_name):
        os.remove(zip_name)
    z = zipfile.ZipFile(zip_name, 'w')
    if os.path.isdir(file_path + str(id)):
        for d in os.listdir(file_path + str(id)):
            z.write(file_path + str(id) + os.sep + d, d)
        z.close()
    return 'zip' + str(id) + '.zip'
