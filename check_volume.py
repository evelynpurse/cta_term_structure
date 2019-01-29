#在表格中添加一列，记录主力合约的成交量
import rqdatac as rq
from rqdatac import *
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

rq.init()
#获取所有品种
cat_list=pd.read_csv("cat_list.csv",header=None,index_col=0)
cat_list=pd.Series(cat_list.groupby(cat_list.iloc[:,0]).count().index)
time_index=pd.read_csv("cat_all_price.csv",index_col=0).index
check_vol=pd.DataFrame(index=time_index)
for j in range(0,len(cat_list)):
    print(cat_list[j])
    # 获取主力合约信息
    domain = pd.read_csv(cat_list[j]+".csv", index_col=0)
    # 获取单个合约的成交量
    volume_history = pd.read_csv(cat_list[j]+"price&volume.csv", index_col=0)
    for i in range(0, len(domain)):
        id = domain.ix[i, 'dominant']
        date=domain.ix[i,:].name
        volume = volume_history.ix[date, "volume" + id]
        domain.ix[i, 'volume'] = volume
    #判断前20天的成交量平均值是否大于10000手，是就返回True
    for k in range(20,len(domain)):
        if(domain.ix[k-20:k,'volume'].mean()>10000):
            domain.ix[k,'vol_check']=True
        else:
            domain.ix[k,'vol_check']=None
    #domain.to_csv(cat_list[j]+"_domain_price_volume.csv")
    check_vol=check_vol.join(domain.ix[:,'vol_check'],how='outer',rsuffix=cat_list[j])
check_vol=check_vol.rename(columns={'vol_check':'vol_checkA'})
col_name=pd.Series(check_vol.columns.values)
col_name=col_name.str.slice(9,len(col_name))
check_vol.columns=col_name
check_vol.to_csv("check_vol.csv")




