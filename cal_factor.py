#计算每个品种的期限结构因子 TS1 TS2 TS3 TS4
import rqdatac as rq
from rqdatac import *
import pandas as pd
import math
import numpy as np
from datetime import datetime , timedelta
rq.init()

startdate=pd.to_datetime('20050104')
enddate=pd.to_datetime('20170120')
#获取所有品种
cat_list=pd.read_csv("cat_list.csv",header=None,index_col=0)
cat_list=pd.Series(cat_list.groupby(cat_list.iloc[:,0]).count().index)

future_info=pd.read_csv("future_info.csv",index_col=0)
future_info1=future_info.set_index(['order_book_id'])

#遍历每个品种
for j in range(0,len(cat_list)):
    # 获取近月远月合约id以及收盘价
    id_list = pd.read_csv(cat_list[j]+"_factor_id.csv", index_col=0)
    price_list = pd.read_csv(cat_list[j]+"price&volume.csv", index_col=0)
    # 新建一个df用来存储展期收益率
    df = pd.DataFrame(columns={'TS1', 'TS2', 'TS3', 'TS4'}, index=id_list.index)
    # 计算TS1 近月与远月
    for i in range(0, len(id_list)):
        trading_date = pd.to_datetime(id_list.index.values[i])
        print(trading_date)
        # 近月合约id
        near_id = id_list.ix[i, 'near1']
        # 远月合约id取near2
        far_id = id_list.ix[i, 'near2']
        # 判断在这一天是否有可以交易的合约
        if (isinstance(near_id, str) & isinstance(far_id, str)):
            if (near_id == far_id):
                df.ix[i, 'TS1'] = None
            else:
                # 近月合约在t时刻的收盘价
                near_price = price_list.ix[i, "close" + near_id]
                # 远月合约在t时刻的收盘价
                far_price = price_list.ix[i, "close" + far_id]
                # 获取交割日期
                # 近月合约的交割日期
                near_mature = pd.to_datetime(future_info1.ix[near_id, 'maturity_date'])
                # 远月合约的交割日期
                far_mature = pd.to_datetime(future_info1.ix[far_id, 'maturity_date'])
                # 计算展期收益率TS1
                if((near_price!=0)&(far_price!=0)):
                    df.ix[i, 'TS1'] = 365 * (math.log(near_price) - math.log(far_price)) / ((far_mature - near_mature).days)
    # TS2 近月与主力
    for i in range(0, len(id_list)):
        trading_date = pd.to_datetime(id_list.index.values[i])
        print(trading_date)
        # 近月合约id
        near_id = id_list.ix[i, 'near1']
        # 远月取主力合约id
        far_id = id_list.ix[i, 'vol1']
        # 判断在这一天是否有可以交易的合约
        if (isinstance(near_id, str) & isinstance(far_id, str)):
            if (near_id == far_id):
                df.ix[i, 'TS2'] = None
            else:
                # 近月合约在t时刻的收盘价
                near_price = price_list.ix[i, "close" + near_id]
                # 远月合约在t时刻的收盘价
                far_price = price_list.ix[i, "close" + far_id]
                # 获取交割日期
                # 近月合约的交割日期
                near_mature = pd.to_datetime(future_info1.ix[near_id, 'maturity_date'])
                # 远月合约的交割日期
                far_mature = pd.to_datetime(future_info1.ix[far_id, 'maturity_date'])
                # 计算展期收益率TS2
                if ((near_price != 0 )& (far_price != 0)):
                    df.ix[i, 'TS2'] = 365 * (math.log(near_price) - math.log(far_price)) / ((far_mature - near_mature).days)
    # TS3 近月和最远月
    for i in range(0, len(id_list)):
        trading_date = pd.to_datetime(id_list.index.values[i])
        print(trading_date)
        # 近月合约id
        near_id = id_list.ix[i, 'near1']
        # 远月取最远月id
        far_id = id_list.ix[i, 'far']
        # 判断在这一天是否有可以交易的合约
        if (isinstance(near_id, str) & isinstance(far_id, str)):
            if (near_id == far_id):
                df.ix[i, 'TS3'] = None
            else:
                # 近月合约在t时刻的收盘价
                near_price = price_list.ix[i, "close" + near_id]
                # 远月合约在t时刻的收盘价
                far_price = price_list.ix[i, "close" + far_id]
                # 获取交割日期
                # 近月合约的交割日期
                near_mature = pd.to_datetime(future_info1.ix[near_id, 'maturity_date'])
                # 远月合约的交割日期
                far_mature = pd.to_datetime(future_info1.ix[far_id, 'maturity_date'])
                # 计算展期收益率TS2
                if ((near_price != 0) & (far_price != 0)):
                    df.ix[i, 'TS3'] = 365 * (math.log(near_price) - math.log(far_price)) / ((far_mature - near_mature).days)
    # TS4 主力和次主力
    for i in range(0, len(id_list)):
        trading_date = pd.to_datetime(id_list.index.values[i])
        print(trading_date)
        # 近月id取主力id
        near_id = id_list.ix[i, 'vol1']
        # 远月id取次主力
        far_id = id_list.ix[i, 'vol2']
        # 判断在这一天是否有可以交易的合约
        if (isinstance(near_id, str) & isinstance(far_id, str)):
            if (near_id == far_id):
                df.ix[i, 'TS4'] = None
            else:
                # 近月合约在t时刻的收盘价
                near_price = price_list.ix[i, "close" + near_id]
                # 远月合约在t时刻的收盘价
                far_price = price_list.ix[i, "close" + far_id]
                # 获取交割日期
                # 近月合约的交割日期
                near_mature = pd.to_datetime(future_info1.ix[near_id, 'maturity_date'])
                # 远月合约的交割日期
                far_mature = pd.to_datetime(future_info1.ix[far_id, 'maturity_date'])
                # 计算展期收益率TS4
                if ((near_price != 0) & (far_price != 0)):
                    df.ix[i, 'TS4'] = 365 * (math.log(near_price) - math.log(far_price)) / ((far_mature - near_mature).days)
    df.to_csv(cat_list[j]+"roll_rt.csv")
