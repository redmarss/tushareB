import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
import tushare as ts

pd=ts.get_k_data('600000','2018-05-01','2018-05-31')

pd.index=pd['date']
pd=pd.iloc[:,1:5]
print(pd)

plt.plot(pd)
plt.show()




