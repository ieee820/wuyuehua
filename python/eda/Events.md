分别截取时间的日、星期、时刻，作为三个新变量，与原来的events表格合并，成为表events1
```
##Events
# coding = utf-8
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import time

events = pd.read_csv('kaggledata/events.csv')

print events.ix[0:5,:]
event_num=events.groupby(["device_id"]).count()['event_id'].copy(deep=True)
print event_num[0:5]

timestamp=events['timestamp'].copy(deep=True)
timestamp_format=map(lambda x: time.localtime(time.mktime(time.strptime(x,"%Y-%m-%d %H:%M:%S"))),timestamp)
tday=map(lambda x:time.strftime('%Y-%m-%d',x),timestamp_format)##extract the day of a month
tweek=map(lambda x:time.strftime('%a',x),timestamp_format)### extract the day of a week
thour=map(lambda x:time.strftime('%H',x),timestamp_format)###extract the Hour of a day

events1=events.copy(deep=True)
events1['tday']=tday
events1['tweek']=tweek
events1['thour']=thour
print events1.ix[0:5,:]

events1.to_csv('kaggledata/events1.csv')
```

![test pic](/python/eda/pic_events/events1.png)

#1、不同时间，用户登录情况
##不同日期
```
p=events1.thour.value_counts().sort_index().plot(kind='bar',figsize=(15,6),rot=0)
_=p.set_xlabel('Hour'),p.set_ylabel('Count')
plt.title('Hour')
plt.show()
x=events1.thour.value_counts()
print x
```

![test pic](/python/eda/pic_events/date_data.png)

![test pic](/python/eda/pic_events/date.png)

大部分集中在5月1日--5月7日之间

##不同时段
```
events1= pd.read_csv('kaggledata/events1.csv')
## when did people use their devices?
events2=events1.copy(deep=True)
events2['thour']=map(lambda x: '%02.f:00-%02.f:59 ' % (x,x),events1.thour)
count=events2.thour.value_counts().sort_index()
count_prop=count/count.sum()
count_prop1=map(lambda x:'%.2f %%'%(x*100),count_prop)
count_prop2=pd.Series(count_prop1,index=count_prop.index)

p=events2.thour.value_counts().sort_index().plot(kind='bar',figsize=(10,5),rot=0)
_=p.set_xlabel('Hour'),p.set_ylabel('Count')
plt.title('When did people use their devices in a day?')
plt.xticks(rotation=45,fontsize=6.5,weight='bold')
p1=p.twinx()
p1.plot(p.get_xticks(),count_prop*100, linestyle='-', marker='.', linewidth=2.0,color='g')
p1.set_ylabel('Proportion:(%)')
plt.show()
```
不同时段流量计数，如下：

![test pic](/python/eda/pic_events/thout_data.png)

不同时段流量的百分比，如下：

![test pic](/python/eda/pic_events/thout_data1.png)

不同时段流量计数、百分比图，如下：

![test pic](/python/eda/pic_events/thout.png)
