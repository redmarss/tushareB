#!/home/mjiang/anaconda3/bin/python3.6

import tushare
import tushare.stock.billboard as billboard
import pandas as pd

pd.set_option('display.height',1000)
pd.set_option('display.max_rows',500)
pd.set_option('display.max_columns',500)
pd.set_option('display.width',1000)

print(billboard.lhb_detail('000063', '2018-06-25'))