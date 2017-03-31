# -*- coding: utf-8 -*-
# @Author: HaonanWu
# @Date:   2017-03-18 10:34:37
# @Last Modified by:   HaonanWu
# @Last Modified time: 2017-03-18 10:34:44

import json
import zipfile, os

def keep_unique(li):
    list_set = set(map(json.dumps, li))
    return map(json.loads, list(list_set))

def make_zip(file_path, id):
    zip_name = file_path + 'zip' + str(id) + '.zip'
    if os.path.exists(zip_name):
        return 'zip' + str(id) + '.zip'
    z = zipfile.ZipFile(zip_name, 'w')
    if os.path.isdir(file_path + str(id)):
        for d in os.listdir(file_path + str(id)):
            z.write(file_path + str(id) + os.sep + d, d)
        z.close()
    return 'zip' + str(id) + '.zip'
