from crawler.print_tree import *
import requests, json
import string


def crawle_douban(method):
    if method == 'true':
        html = r'https://api.douban.com/v2/movie/top250?start={page}'
        i = 1
        p = 1
        while p <= 5:
            try:
                hjson = json.loads(requests.get(html.format(page=(p - 1) * 20)).text)
            except Exception as e:
                return
            # 处理json，具体返回样例参照豆瓣API即可，输出格式：  排行：电影中文名---英文名（年代）
            for key in hjson['subjects']:
                line = [str(i), key['title'], key['original_title'], key['year']]
                csv_line(line, 0, 0, 0, [])
                i += 1
            p += 1
    else:
        html = "https://api.douban.com/v2/book/search"
        book_tag_lists = ['计算机', '机器学习', 'linux', 'android', '数据库', '互联网']
        i = 1
        p = 0
        while p < len(book_tag_lists):
            dic = {'tag': book_tag_lists[p]}
            try:
                hjson = json.loads(requests.get(html, dic).text)
            except Exception as e:
                print(e)
            # 处理json，具体返回样例参照豆瓣API即可
            book_list = hjson['books']
            book_list = sorted(book_list, key=lambda x: float(x['rating']['average']), reverse=True)
            for key in book_list:
                line = [str(i), key['id'], key['title'], key['author'][0], key['rating']['average']]
                csv_line(line, 0, 1, 0, [])
                i += 1
            p += 1
