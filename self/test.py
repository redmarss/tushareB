#!/usr/bin/python3
# -*- coding: utf-8 -*-

import self.longhu.mysqlConn as nm
import tushare as ts

code="600223"
date="2018-06-15"
t=ts.lhb_detail(code,date)
for i in t:
    print(i)











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






