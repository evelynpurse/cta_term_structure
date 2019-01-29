import rqdatac as rq
from rqdatac import *
import pandas as pd
import numpy as np
from datetime import datetime , timedelta
rq.init()

startdate=pd.to_datetime('20050104')
enddate=pd.to_datetime('20170120')
#获取所有品种
cat_list=pd.read_csv("cat_list.csv",header=None,index_col=0)
cat_list=pd.Series(cat_list.groupby(cat_list.iloc[:,0]).count().index)
time_index=pd.read_csv("cat_all_price.csv",index_col=0).index
#获取所有合约的基本信息
future_info=pd.read_csv("future_info.csv",index_col=0)
future_info1=future_info.set_index(['order_book_id'])
#遍历所有品种
for i in range(0,len(cat_list)):
    # 新建一个数据框，记录交易量第一第二，近月、次近月、最远月的合约id
    df = pd.DataFrame(columns={'vol1', 'vol2', 'near1', 'near2', 'far'}, index=time_index)
    #获取单个品种所有合约
    price_volume=pd.read_csv(cat_list[i]+"price&volume.csv",index_col=0)
    #新建一个数据框，排序
    df_vol=pd.DataFrame()
    for j in range(1,price_volume.shape[1],2):
        df_vol=df_vol.join(price_volume.ix[:,j],how='outer')
    cat_id_list = pd.Series(df_vol.columns.values)
    cat_id_list = cat_id_list.str.slice(6, len(cat_id_list))
    df_vol.columns = cat_id_list
    #遍历每个日期
    for j in range(0,len(df_vol)):
        print(time_index[j])
        sr_vol=df_vol.ix[j,:].dropna()
        if(sr_vol.size!=0):
            if(sr_vol.size==1):
                df.ix[j, 'vol1']=sr_vol.index.values[0]
                df.ix[j, 'vol2'] = sr_vol.index.values[0]
            else:
                # 选出主力、次主力
                df.ix[j, 'vol1'] = sr_vol.sort_values(ascending=False).head(2).index.values[0]
                df.ix[j, 'vol2'] = sr_vol.sort_values(ascending=False).head(2).index.values[1]

    mature=future_info1.ix[cat_id_list,['maturity_date','listed_date']]
    #获得当期可交易的列表
    for j in range(0,len(time_index)):
        print(time_index[j])
        mature1 = mature[(mature.maturity_date > time_index[j]) & (mature.listed_date < time_index[j])]
        if(len(mature1)!=0):
            if(len(mature1)==1):
                df.ix[j, 'near1'] = mature1.index.values[0]
                df.ix[j, 'near2'] = mature1.index.values[0]
                df.ix[j, 'far'] = mature1.index.values[0]
            else:
                # 最近月
                df.ix[j, 'near1'] = mature1['maturity_date'].sort_values(ascending=True).head(2).index.values[0]
                # 次近月
                df.ix[j, 'near2'] = mature1['maturity_date'].sort_values(ascending=True).head(2).index.values[1]
                # 最远月
                df.ix[j, 'far'] = mature1['maturity_date'].sort_values(ascending=False).head(1).index.values[0]
    df.to_csv(cat_list[i]+"_factor_id.csv")





























