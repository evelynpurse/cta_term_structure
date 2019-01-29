import numpy as np
import pandas as pd
import datetime
from datetime import datetime , timedelta
benchmark='NH0100'
benchmark_history=pd.read_csv("NH.csv",index_col=0)
cat_list=pd.read_csv("cat_list.csv",header=None,index_col=0)
cat_list=pd.Series(cat_list.groupby(cat_list.iloc[:,0]).count().index)
cat_all_price=pd.read_csv("cat_all_price.csv",index_col=0)
cat_all_price=pd.DataFrame(data=cat_all_price.values,index=cat_all_price.index,columns=cat_list)
time_index=pd.read_csv("cat_all_price.csv",index_col=0).index
startdate=pd.to_datetime('20050104')
enddate=pd.to_datetime('20170120')
#计算benchmark持有期收益
yearly_rt=(benchmark_history.ix[len(benchmark_history)-1,'close']/benchmark_history.ix[0,'close'])**(365 / 4399)
#建立函数，计算收益率
#多头组合
def long_rt(H,TS):
    port = pd.read_csv(TS + "_port.csv", index_col=0)
    accounts = pd.DataFrame(index=time_index, columns={'period_rt'})
    # 遍历时间
    for i in range(20, len(port) - H, H):
        a = 0
        b = 0
        # 遍历品种，计算组合在H时间内的收益率
        for j in range(0, port.shape[1]):
            if (port.ix[i, j] == 1):
                a += cat_all_price.ix[i + H, j]
                b += cat_all_price.ix[i, j]
            if (j == port.shape[1] - 1):
                accounts.ix[i + H, 'period_rt'] = (a - b) / b
    accounts = accounts.dropna()
    accounts['rt1'] = accounts.add(1)
    holding_rt = accounts.ix[:, 'rt1'].cumprod().tail(1).values
    # 计算平均收益率
    expected_rt = accounts.ix[:, 'period_rt'].mean()
    # 计算标准差
    std_rt = accounts.ix[:, 'period_rt'].std()
    # 计算年化收益率
    yearly_rt = (holding_rt) ** (365 / 4399) - 1
    # 计算持仓胜率
    positive_rt_count = 0
    negative_rt_count = 0
    for k in range(0, len(accounts)):
        if (accounts.ix[k, 'period_rt'] > 0):
            positive_rt_count = positive_rt_count + 1
        else:
            negative_rt_count = negative_rt_count + 1
    win_rate = positive_rt_count / len(accounts)
    # 计算风险收益比
    risk_rt = yearly_rt / ((std_rt * (240 / H)) ** 0.5)
    performance = pd.DataFrame(data=[expected_rt, yearly_rt[0], risk_rt[0], win_rate])
    return accounts.ix[:'period_rt']
#空头组合
def short_rt(H,TS):
    port = pd.read_csv(TS + "_port.csv", index_col=0)
    accounts = pd.DataFrame(index=time_index, columns={'period_rt'})
    # 遍历时间
    for i in range(20, len(port) - H, H):
        a = 0
        b = 0
        # 遍历品种，计算组合在H时间内的收益率
        for j in range(0, port.shape[1]):
            if (port.ix[i, j] == -1):
                a += cat_all_price.ix[i + H, j]
                b += cat_all_price.ix[i, j]
            if (j == port.shape[1] - 1):
                accounts.ix[i + H, 'period_rt'] = (a - b) / b
    accounts = accounts.dropna()
    accounts['rt1'] = accounts.add(1)
    holding_rt = accounts.ix[:, 'rt1'].cumprod().tail(1).values
    # 计算平均收益率
    expected_rt = accounts.ix[:, 'period_rt'].mean()
    # 计算标准差
    std_rt = accounts.ix[:, 'period_rt'].std()
    # 计算年化收益率
    yearly_rt = (holding_rt) ** (365 / 4399) - 1
    # 计算持仓胜率
    positive_rt_count = 0
    negative_rt_count = 0
    for k in range(0, len(accounts)):
        if (accounts.ix[k, 'period_rt'] > 0):
            positive_rt_count = positive_rt_count + 1
        else:
            negative_rt_count = negative_rt_count + 1
    win_rate = positive_rt_count / len(accounts)
    # 计算风险收益比
    risk_rt = yearly_rt / ((std_rt * (240 / H)) ** 0.5)
    performance = pd.DataFrame(data=[expected_rt, yearly_rt[0], risk_rt[0], win_rate])
    return accounts.ix[:,'period_rt']

def longshort_rt(H,TS):
    port = pd.read_csv(TS + "_port.csv", index_col=0)
    accounts = pd.DataFrame(index=time_index, columns={'period_rt'})
    # 遍历时间
    for i in range(20, len(port) - H, H):
        a = 0
        b = 0
        c=0
        d=0
        # 遍历品种，计算组合在H时间内的收益率
        for j in range(0, port.shape[1]):
            if(port.ix[i,j]==1):
                a += cat_all_price.ix[i + H, j]
                b += cat_all_price.ix[i, j]
            if (port.ix[i, j] == -1):
                c += cat_all_price.ix[i + H, j]
                d += cat_all_price.ix[i, j]
            if (j == port.shape[1] - 1):
                accounts.ix[i + H, 'period_rt'] = (a-b)/b+(d-c)/c
    accounts = accounts.dropna()
    accounts['rt1'] = accounts.add(1)
    holding_rt = accounts.ix[:, 'rt1'].cumprod().tail(1).values
    # 计算平均收益率
    expected_rt = accounts.ix[:, 'period_rt'].mean()
    # 计算标准差
    std_rt = accounts.ix[:, 'period_rt'].std()
    # 计算年化收益率
    yearly_rt = (holding_rt) ** (365 / 4399) - 1
    # 计算持仓胜率
    positive_rt_count = 0
    negative_rt_count = 0
    for k in range(0, len(accounts)):
        if (accounts.ix[k, 'period_rt'] > 0):
            positive_rt_count = positive_rt_count + 1
        else:
            negative_rt_count = negative_rt_count + 1
    win_rate = positive_rt_count / len(accounts)
    # 计算风险收益比
    risk_rt = yearly_rt / ((std_rt * (240 / H)) ** 0.5)
    performance = pd.DataFrame(data=[expected_rt, yearly_rt[0], risk_rt[0], win_rate])
    return accounts.ix[:,'period_rt']

def calculate_benchmark_rt(H):
    colname = "H=" + str(H)
    for i in range(H, len(benchmark_history) - H, H):
        benchmark_history.ix[i + H, colname] = (benchmark_history.ix[i + H, 'close'] - benchmark_history.ix[i, 'close']) / benchmark_history.ix[i, 'close']
    rt = benchmark_history.ix[:, colname].dropna()
    rt = rt.to_frame()
    rt['rt1'] = rt[colname].add(1)
    holding_rt = rt['rt1'].cumprod()
    return  holding_rt

#calculate_benchmark_rt(20).to_csv("benchmark1.csv")
#long_rt(20,"TS2").to_csv("long_20_TS2.csv")
#short_rt(20,"TS2").to_csv("short_20_TS2.csv")
longshort_rt(20,"TS2").to_csv("longshort_20_TS2.csv")




