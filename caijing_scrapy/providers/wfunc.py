# -*- coding: utf-8 -*-

# 扩展函数
# by wooght 2017-11

import time
import re
import sys,io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

#字符串时间转换为时间暨
def time_num(str,format):
    timeArray = time.strptime(str, format)
    timestamp = time.mktime(timeArray)
    return int(timestamp)

def today():
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime()) #格式化时间 2017-10-23 17:10:54

#雪球时间匹配
def search_time(str):
    str_search=re.search(r'\D*(\d{4}-\d{2}-\d{2} .*)',str)
    if(str_search):
        return str_search.group(1)
    else:
        str_search = re.search(r'\D*(\d{2}-\d{2} .*)',str)
        if(str_search):
            year = time.strftime("%Y")
            str = year+'-'+str_search.group(1)
            return str
        else:
            return today()

#新浪新闻事件获取
def sina_get_time(strr):
    time_re = re.search(r'(\d{4})\D*(\d{2})\D*(\d{2})\D*(\d{2})\:(\d{2})',strr)
    if(time_re):
        time_str = time_re.group(1)+'-'+time_re.group(2)+'-'+time_re.group(3)+' '+time_re.group(4)+':'+time_re.group(5)+':00'
    else:
        time_str = today()
    return time_num(time_str,"%Y-%m-%d %H:%M:%S")

#删除html标签
def delete_html(str):
    re_str = re.sub(r'<[^>]*>','',str.strip())
    return re_str
