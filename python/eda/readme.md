```
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
gender_age_train=pd.read_csv('kaggledata/gender_age_train.csv')
gender_age_test=pd.read_csv('kaggledata/gender_age_test.csv')
phone_brand_device_model=pd.read_csv('kaggledata/phone_brand_device_model.csv')
events=pd.read_csv('kaggledata/events.csv')
app_events=pd.read_csv('kaggledata/app_events.csv')
app_labels=pd.read_csv('kaggledata/app_labels.csv')
```

一、用户属性特征和手机品牌关系研究

```
Gender_age_train & phone_brand_device_model à train_phone
##merge gender_age_train and phone_brand_device_model as train_phone
phone_brand_device_model_1=phone_brand_device_model.drop_duplicates()
###change phone_brand language from chinese to english in phone_brand_device_model
phone_brand_cn=pd.read_csv('kaggledata/phone_brand_cn.csv')
phone_brand_translate=pd.read_csv('kaggledata/phone_brand_translate.csv')
phone_brand_cn_en=pd.merge(phone_brand_cn,phone_brand_translate,on='phone_brand_cn',how='left')
phone_brand_cn_en.to_csv('kaggledata/phone_brand_cn_en.csv')
phone_brand_cn_en1=pd.read_csv('kaggledata/phone_brand_cn_en1.csv')
##
phone_brand_device_model_1=phone_brand_device_model.drop_duplicates()
phone_brand_new1=pd.merge(pd.DataFrame(phone_brand_device_model_1.ix[:,'phone_brand']),phone_brand_cn_en1,on='phone_brand',how='left')
phone_brand_device_model_2=phone_brand_device_model_1.copy(deep=True)
phone_brand_device_model_2.ix[:,'phone_brand']=phone_brand_new1.ix[:,'phone_brand_en']
##merge gender_age_train and phone_brand_device_model as train_phone
train_phone=pd.merge(gender_age_train,phone_brand_device_model_2,on='device_id',how='left')
```

train_phone表结构：
```
print train_phone.ix[0:5,:]
print train_phone.shape
```

![说明pic](/pic/train_phone.png)

1、性别特征 Gender：

```
#train : gender
x=train_phone.gender.value_counts()
print x
p=train_phone.gender.value_counts().plot(kind='bar',figsize=(15,6),rot=0)
_=p.set_xlabel('Gender'),p.set_ylabel('Count')
plt.show()
```

![test pic](/pic/basic1.png)

2、群组特征 Group:
train : group
```
x=train_phone.group.value_counts().sort_index()
print x
p=train_phone.group.value_counts().sort_index().plot(kind='bar',figsize=(15,6),rot=0)
_=p.set_xlabel('Group'),p.set_ylabel('Count')
plt.show()
```
![test pic](/pic/group.png)
![test pic](/pic/basic2.png)


3、手机品牌特征 Phone_brand：

```
#phone_brand
phone_brand_counts=train_phone.phone_brand.value_counts()
phone_brand_counts_prop=phone_brand_counts/sum(phone_brand_counts)
phone_brand_counts_prop=np.array(phone_brand_counts_prop)
phone_brand_counts_prop1=pd.Series(np.cumsum(phone_brand_counts_prop),index=phone_brand_counts.index)
print phone_brand_counts
print phone_brand_counts_prop1
```

各手机品牌使用情况如下：
![test pic](/pic/phone_brand.png)

按被使用次数进行排序后，计算器累计和：可以发现90%以上的人使用的手机集中前十个品牌。
![test pic](/pic/phone_brand_prop_cumsum.png)




4、Phone_brand vs Group

将使用次数排序不在前十的手机品牌分组为‘Others’

```
##change the left phone brands except the first 10 to 'else' class
train_phone1=train_phone.copy(deep=True)
name=phone_brand_counts_prop1.index[0:10]
train_phone1.ix[train_phone1.phone_brand.isin(name)==False,'phone_brand']='Others'
print train_phone1.ix[0:5,:]
```
![test pic](/pic/train_phone1.png)


#可以看每一个用户分组中，手机品牌使用占比情况：
```
data =train_phone1.groupby(["group", "phone_brand"]).count()["device_id"].unstack().copy(deep = True)
print data
p = data.div(data.sum(axis = 1), axis = 0).plot.barh(stacked = True, rot = 0, figsize = (15, 8), width = .5)
_ = p.set_xticklabels(""), p.legend(fontsize = 12., loc = "right", ncol = 1, borderpad = -.15)
a_ = p.set_ylabel("Group"), p.set_xlabel("Count")
#plt.show()
```
![test pic](/pic/group_phonebrand.png)

![test pic](/pic/basic3.png)

#可以看每一个品牌下，不同用户群的占比：
```
data =train_phone1.groupby(["phone_brand", "group"]).count()["device_id"].unstack().copy(deep = True)
print data
print data.sum(axis=1)
x= data.div(data.sum(axis = 1), axis = 0)
p=x.plot.barh(stacked = True, rot = 0, figsize = (15, 8), width = .5)
_ = p.set_xticklabels(""), p.legend(fontsize = 12., loc = "right", ncol = 1, borderpad = -.15)
a_ = p.set_ylabel("Phone_brand"), p.set_xlabel("Count")
plt.show()
```

![test pic](/pic/basic4.png)

5、Phone_brand vs gender
#不同品牌的性别比重

## Phone_brand VS Gender
```
data =train_phone1.groupby(["phone_brand", "gender"]).count()["device_id"].unstack().copy(deep = True)
x= data.div(data.sum(axis = 1), axis = 0)
name1=list(name)
name1.append("Others")
x1=pd.DataFrame(x,index=name1)
print x1
p=x1.plot.barh(stacked = True, rot = 0, figsize = (15, 8), width = .5)
_ = p.set_xticklabels(""), p.legend(fontsize =20., loc = "right", ncol = 1, borderpad = -.15)
a_ = p.set_ylabel("Phone_brand"), p.set_xlabel("Count")
plt.show()
```
![test pic](/pic/phonebrand_gender.png)
![test pic](/pic/basic5.png)

#不同性别下 ，各个品牌的比重


|姓名|密码|游戏|
|---|---|----|
|test1|123|hahha|
|test1111|1232|ppp|
