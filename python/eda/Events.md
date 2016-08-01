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

##Events
print events.ix[0:5,:]
event_num=events.groupby(["device_id"]).count()['event_id'].copy(deep=True)
print event_num[0:5]

timestamp=events['timestamp'].copy(deep=True)
timestamp_format=map(lambda x: time.localtime(time.mktime(time.strptime(x,"%Y-%m-%d %H:%M:%S"))),timestamp)
tday=map(lambda x:time.strftime('%d',x),timestamp_format)##extract the day of a month
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


