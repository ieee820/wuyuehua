```
##merge train_phone1 and events1 to train_phone_events
events2=pd.read_csv('kaggledata/events2.csv')
train_phone1=pd.read_csv('kaggledata/train_phone1.csv')
del events2['Unnamed: 0']
del events2['Unnamed: 0.1']
del train_phone1['Unnamed: 0']
print events2.ix[0:5,:]
print train_phone1.ix[0:5,:]
train_phone_events=pd.merge(events2,train_phone1,on='device_id',how='inner')
print train_phone_events.ix[0:5,:]


count=train_phone_events.thour.value_counts().sort_index()
count_prop=count/count.sum()
count_prop1=map(lambda x:'%.2f %%'%(x*100),count_prop)
count_prop2=pd.Series(count_prop1,index=count_prop.index)

p=events2.tday.value_counts().sort_index().plot(kind='bar',figsize=(15,6),rot=0)
_=p.set_xlabel('Date'),p.set_ylabel('Count')
plt.title('Date')
plt.show()

p1=train_phone_events.thour.value_counts().sort_index().plot(kind='bar',figsize=(10,5),rot=0)
_1=p1.set_xlabel('Hour'),p1.set_ylabel('Count')
plt.title('When did people use their devices in a day?')
plt.xticks(rotation=45,fontsize=6,weight='bold')
p2=p1.twinx()
p2.plot(p1.get_xticks(),count_prop*100, linestyle='-', marker='.', linewidth=2.0,color='g')
p2.set_ylabel('Proportion:(%)')
plt.show()

```
![test pic](/python/eda/pic_events/date1.png)

![test pic](/python/eda/pic_events/thour1.png)