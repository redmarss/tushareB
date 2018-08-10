#!/usr/bin/python3
# -*- coding: utf-8 -*-


import self.longhu.anaylzeData as ad
import self.longhu.RunOnce as ro
import self.longhu.globalFunction as gl
import self.longhu.getFromTushare as gt
import tushare as ts
from tushare.stock import cons as ct
import json
#print(ad.anaylzeLonghu('80065939','2017-05-02'))
# ad.getPrice("600000","2018-06-09")
# df=ad.getPrice('600000','2018-06-01',5)
# print(df)
# js=df.to_json(orient='records')
#
# print(js)
# startdate="2017-01-05"
# while startdate<"2017-12-31":
#     startdate=str(gl.diffDay(startdate,1))
#     ad.getData(startdate)
#ad.getData("2018-07-06")
# ad.getAllBroker()
# ad.ScoreBroker('80141202',"600000","2017-05-05")

print(gl.isLimit('600986',5.56,6.11))









    # df[1]=df[1].map(lambda x: x[0])









# request = Request(rv.LHB_URL%(ct.P_TYPE['http'], ct.DOMAINS['em'], "2018-05-22","2018-05-22"))
# text=urlopen(request,timeout=10).read()
# text=text.decode('GBK')
# text=text.split('_1=')[1]
# text=eval(text, type('Dummy', (dict,),
#                      dict(__getitem__ = lambda s, n:n))())
# text=json.dumps(text)
# text=json.loads(text)
# df = pd.DataFrame(text['data'], columns=rv.LHB_TMP_COLS)
# df.columns = rv.LHB_COLS

# request=Request(rv.LHB_SINA_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'], rv.LHB_KINDS[0],
#                                                ct.PAGES['fd'], 30, 1))
# print(rv.LHB_SINA_URL%(ct.P_TYPE['http'], ct.DOMAINS['vsf'], rv.LHB_KINDS[0],
#                                                ct.PAGES['fd'], 30, 1))
# text=urlopen(request,timeout=10).read()
# text=text.decode('GBK')
# html=lxml.html.parse(StringIO(text))
# res = html.xpath("//table[@id=\"dataTable\"]/tr")
# if ct.PY3:
#     sarr = [etree.tostring(node).decode('utf-8') for node in res]
# else:
#     sarr = [etree.tostring(node) for node in res]
# sarr = ''.join(sarr)
# sarr = '<table><table>%s</table></table>'%sarr
# df = pd.read_html(sarr)[0]
# print(df)


# at1.AnalyzeLonghuList("2018-02-22","2018-04-22")
# t=gt.getLastDayDate("2018-05-10")
# ls=at.CreateClass(t[1])
# # for i in range(len(ls)):
# #     print(ls[i])
# print(ls)
# list1=at.getFromSql("2018-05-10")
# at.printDetail(list1)






