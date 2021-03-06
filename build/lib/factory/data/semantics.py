# -*- coding: utf-8 -*-
#
# @method   : 前端语义分析展示数据组装
# @Time     : 2017/12/27
# @Author   : wooght
# @File     : semantics.py

import os
import sys

sys_path = os.path.dirname(__file__)+'/../../'
sys.path.append(sys_path)
from model import topic
from analyse.common import *
from analyse.NLP.participle import pp
from analyse.NLP.semantics import seman

try:
    article_id = sys.argv[1]
except:
    article_id = 47512


class semantics:
    title = ''
    body = ''
    keywords = []
    words = []
    ju = []
    zf = []

    def __init__(self, article_id):
        seman.load('topic.wooght')
        articles_dict = dict(topic.one(article_id))
        self.title = articles_dict['title']
        self.body = articles_dict['body'].strip()
        keywords = pp.tags(self.body, allpos=('n', 'a', 'nt', 'v', 'd', 'ns'))
        for words in keywords:
            ws = [words[0].word.encode('utf-8'), words[0].flag, words[1]]
            self.keywords.append(ws)
        words = pp.flag_cut(self.body, stop_flag=('x', 'ns', 'm'))
        for w in words:
            w_tmp = [w.word.encode('utf-8'), w.flag, 0, 0]
            w_tmp[2] = seman.ask['pos'].get_rate(w.word)
            w_tmp[3] = seman.ask['neg'].get_rate(w.word)
            self.words.append(w_tmp)
        ju = pp.cut_ju(self.body)
        for j in ju:
            fen = get_one(j)
            self.ju.append([j.strip().encode('utf-8'), fen])
        listed_plate, listed_company = get_index(self.body)
        if len(listed_company) > 0:
            for companys in listed_company.items():
                cfen = get_lists(companys[0], ju)
                self.zf.append([companys[0].encode('utf-8'), companys[1], cfen])


wrun = semantics(article_id)
return_dict = {
    'zf': wrun.zf,
    'body': wrun.body.encode('utf-8'),
    'title': wrun.title.encode('utf-8'),
    'ju': wrun.ju,
    'keywords': wrun.keywords,
    'words': wrun.words,
}
# print(sys.getdefaultencoding()) # 输出当前编码
print(return_dict)
