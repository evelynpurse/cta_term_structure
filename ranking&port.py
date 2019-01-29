#计算复权因子，并且计算复权后的各个品种收盘建
import rqdatac as rq
from rqdatac import *
import pandas as pd
import numpy as np
from datetime import datetime , timedelta
rq.init()

check_vol=pd.read_csv("check_vol.csv",index_col=0)
time_index=pd.read_csv("cat_all_price.csv",index_col=0).index
# 获得所有可交易的合约品种
cat_list = pd.read_csv("cat_list.csv", header=None, index_col=0)
cat_list = pd.Series(cat_list.groupby(cat_list.iloc[:, 0]).count().index)

TS1_df=pd.DataFrame(index=time_index)
TS2_df=pd.DataFrame(index=time_index)
TS3_df=pd.DataFrame(index=time_index)
TS4_df=pd.DataFrame(index=time_index)
TS1_port=pd.DataFrame(index=time_index,columns=cat_list)
TS2_port=pd.DataFrame(index=time_index,columns=cat_list)
TS3_port=pd.DataFrame(index=time_index,columns=cat_list)
TS4_port=pd.DataFrame(index=time_index,columns=cat_list)
#将所有因子拼接在一张表内
for i in range(0,len(cat_list)):
    single=pd.read_csv(cat_list[i]+"roll_rt.csv",index_col=0)
    TS1_df=TS1_df.join(single.ix[:,'TS1'],how='outer',rsuffix=cat_list[i])

for i in range(0,len(cat_list)):
    single=pd.read_csv(cat_list[i]+"roll_rt.csv",index_col=0)
    TS2_df=TS2_df.join(single.ix[:,'TS2'],how='outer',rsuffix=cat_list[i])
for i in range(0,len(cat_list)):
    single=pd.read_csv(cat_list[i]+"roll_rt.csv",index_col=0)
    TS3_df=TS3_df.join(single.ix[:,'TS3'],how='outer',rsuffix=cat_list[i])
for i in range(0,len(cat_list)):
    single=pd.read_csv(cat_list[i]+"roll_rt.csv",index_col=0)
    TS4_df=TS4_df.join(single.ix[:,'TS4'],how='outer',rsuffix=cat_list[i])
TS1_df=TS1_df.rename(columns={'TS1':'TS1A'})
TS2_df=TS2_df.rename(columns={'TS2':'TS2A'})
TS3_df=TS3_df.rename(columns={'TS3':'TS3A'})
TS4_df=TS4_df.rename(columns={'TS4':'TS4A'})
TS1_df.to_csv("TS1_df.csv")
TS2_df.to_csv("TS2_df.csv")
TS3_df.to_csv("TS3_df.csv")
TS4_df.to_csv("TS4_df.csv")
#TS1
for i in range(20,len(check_vol)):
   #符合前二十天平均成交量大于一万手
   cat_avail_list=check_vol.ix[i,:].dropna()
   #每个品种提取因子值
   for j in range(0,len(cat_avail_list)):
       id1=cat_avail_list.index.values[j]
       cat_avail_list[j]=TS1_df.ix[i,"TS1"+id1]
   #因子值排序，提取前20%记为1.后20%记为-1
   port_size = round(0.2 * cat_avail_list.size)
   tail_port=cat_avail_list.sort_values(ascending=True).head(port_size)
   head_port=cat_avail_list.sort_values(ascending=True).tail(port_size)
   #在TS1_port中记录前20%的品种
   for j in range(0,len(head_port)):
       id2=head_port.index[j]
       TS1_port.ix[i,id2]=1
   for j in range(0,len(tail_port)):
       id3=tail_port.index[j]
       TS1_port.ix[i,id3]=-1
#TS2
for i in range(20,len(check_vol)):
   #符合前二十天平均成交量大于一万手
   cat_avail_list=check_vol.ix[i,:].dropna()
   #每个品种提取因子值
   for j in range(0,len(cat_avail_list)):
       id1=cat_avail_list.index.values[j]
       cat_avail_list[j]=TS2_df.ix[i,"TS2"+id1]
   #因子值排序，提取前20%记为1.后20%记为-1
   port_size = round(0.2 * cat_avail_list.size)
   tail_port=cat_avail_list.sort_values(ascending=True).head(port_size)
   head_port=cat_avail_list.sort_values(ascending=True).tail(port_size)
   #在TS1_port中记录前20%的品种
   for j in range(0,len(head_port)):
       id2=head_port.index[j]
       TS2_port.ix[i,id2]=1
   for j in range(0,len(tail_port)):
       id3=tail_port.index[j]
       TS2_port.ix[i,id3]=-1
#TS3
for i in range(20,len(check_vol)):
   #符合前二十天平均成交量大于一万手
   cat_avail_list=check_vol.ix[i,:].dropna()
   #每个品种提取因子值
   for j in range(0,len(cat_avail_list)):
       id1=cat_avail_list.index.values[j]
       cat_avail_list[j]=TS3_df.ix[i,"TS3"+id1]
   #因子值排序，提取前20%记为1.后20%记为-1
   port_size = round(0.2 * cat_avail_list.size)
   tail_port=cat_avail_list.sort_values(ascending=True).head(port_size)
   head_port=cat_avail_list.sort_values(ascending=True).tail(port_size)
   #在TS1_port中记录前20%的品种
   for j in range(0,len(head_port)):
       id2=head_port.index[j]
       TS3_port.ix[i,id2]=1
   for j in range(0,len(tail_port)):
       id3=tail_port.index[j]
       TS3_port.ix[i,id3]=-1
#TS4
for i in range(20,len(check_vol)):
   #符合前二十天平均成交量大于一万手
   cat_avail_list=check_vol.ix[i,:].dropna()
   #每个品种提取因子值
   for j in range(0,len(cat_avail_list)):
       id1=cat_avail_list.index.values[j]
       cat_avail_list[j]=TS4_df.ix[i,"TS4"+id1]
   #因子值排序，提取前20%记为1.后20%记为-1
   port_size = round(0.2 * cat_avail_list.size)
   tail_port=cat_avail_list.sort_values(ascending=True).head(port_size)
   head_port=cat_avail_list.sort_values(ascending=True).tail(port_size)
   #在TS1_port中记录前20%的品种
   for j in range(0,len(head_port)):
       id2=head_port.index[j]
       TS4_port.ix[i,id2]=1
   for j in range(0,len(tail_port)):
       id3=tail_port.index[j]
       TS4_port.ix[i,id3]=-1
TS1_port.to_csv("TS1_port.csv")
TS2_port.to_csv("TS2_port.csv")
TS3_port.to_csv("TS3_port.csv")
TS4_port.to_csv("TS4_port.csv")



