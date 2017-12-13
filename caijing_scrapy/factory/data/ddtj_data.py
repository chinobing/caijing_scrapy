#encoding utf-8
# ##################################
# 大单统计数据组装
# by wooght
# 2017-11
# ##################################
import sys
sys.path.append('F:\homestead\scripy_wooght\caijing_scrapy\caijing_scrapy')
from factory.basedata import basedata
import providers.wfunc as wfunc
import os,json
import model.Db as T
#获取参数股票代码
try:
    code_id = sys.argv[1]
except:
    code_id = 601318

class ddtj_data(basedata):

    def select_ddtj(self):
        quotes_data = self.select_quotes(code_id)
        s = T.select([T.ddtj.c.totalamt,T.ddtj.c.totalamtpct,T.ddtj.c.totalvol,T.ddtj.c.totalvolpct,
                    T.ddtj.c.stockvol,T.ddtj.c.stockamt,T.ddtj.c.opendate,T.ddtj.c.kuvolume,T.ddtj.c.kdvolume]).where(T.ddtj.c.code_id==code_id)
        r = T.conn.execute(s)
        data_arr = []
        for i in r.fetchall():
            #数据库查询得到字典
            data_arr.append(dict(i))
        pandas_ddtj = self.pd.DataFrame(data_arr)
        pandas_ddtj['datatime'] = self.pd.to_datetime(pandas_ddtj['opendate'],format='%Y-%m-%d')
        pandas_ddtj['dk_contrast'] = pandas_ddtj['kuvolume'] - pandas_ddtj['kdvolume']
        pandas_ddtj['kdvolume'] = -pandas_ddtj['kdvolume']
        quotes_data['datatime'] = self.pd.to_datetime(quotes_data['datatime'],format='%Y-%m-%d')
        del pandas_ddtj['opendate']
        pandas_ddtj = self.pd.merge(pandas_ddtj,quotes_data,on=['datatime'],how='left')
        pandas_ddtj = pandas_ddtj.sort_values(by='datatime',ascending=True)
        result = self.web_data(pandas_ddtj,'datatime',columns=['zd_range','dk_contrast','kuvolume','kdvolume'])
        return result

a = ddtj_data()
b = a.select_ddtj()
print(b)