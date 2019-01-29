import rqdatac as rq
from rqdatac import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

rq.init()

startdate = pd.to_datetime('20050104')
enddate = pd.to_datetime('20170120')
# 获得所有可交易的合约品种
cat_list = pd.read_csv("cat_list.csv", header=None, index_col=0)
cat_list = pd.Series(cat_list.groupby(cat_list.iloc[:, 0]).count().index)
# 获得所有交易日
time_index = pd.read_csv("cat_all_price.csv", index_col=0).index

# 获得合约基础信息（交易代码、交割时间、品种）
future_info = all_instruments(type='Future')
future_info = future_info[['maturity_date', 'underlying_symbol', 'order_book_id','listed_date']]

# 剔除S GN IC IF IH TF TS T AP CY
future_info = future_info[~future_info['underlying_symbol'].isin(['S'])]
future_info = future_info[~future_info['underlying_symbol'].isin(['GN'])]
future_info = future_info[~future_info['underlying_symbol'].isin(['IC'])]
future_info = future_info[~future_info['underlying_symbol'].isin(['IF'])]
future_info = future_info[~future_info['underlying_symbol'].isin(['TH'])]
future_info = future_info[~future_info['underlying_symbol'].isin(['TS'])]
future_info = future_info[~future_info['underlying_symbol'].isin(['T'])]
future_info = future_info[~future_info['underlying_symbol'].isin(['AP'])]
future_info = future_info[~future_info['underlying_symbol'].isin(['CY'])]
# 剔除指数
future_info = future_info[~future_info['maturity_date'].isin(['0000-00-00'])]
future_info = future_info[~future_info['listed_date'].isin(['0000-00-00'])]
#转化为日期
future_info['listed_date']=pd.to_datetime(future_info['listed_date'],format='%Y-%m-%d')
future_info['maturity_date']=pd.to_datetime(future_info['maturity_date'],format='%Y-%m-%d')



#获取所有合约
order_book_list=future_info.groupby(future_info['order_book_id']).count().index.values



for i in range(0,len(cat_list)):
    order_price_volume = pd.DataFrame(index=time_index)
    cat_id_list = future_info.groupby(['underlying_symbol', 'order_book_id']).count().ix[cat_list[i], :].index.values
    #遍历每个品种的所有合约
    for j in range(0,len(cat_id_list)):
        print(cat_id_list[j])
        order_single = get_price(cat_id_list[j], start_date=startdate, end_date=enddate, fields=['close', 'volume'])
        order_price_volume = order_price_volume.join(order_single, how='outer', rsuffix=cat_id_list[j])
    order_price_volume=order_price_volume.rename(columns={'volume':'volume'+cat_id_list[0],'close':'close'+cat_id_list[0]})
    order_price_volume.to_csv(cat_list[i]+"price&volume.csv")
future_info.to_csv("future_info.csv")