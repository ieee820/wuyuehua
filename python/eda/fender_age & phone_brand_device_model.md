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

#一、用户属性特征和手机品牌关系研究

```
##merge Gender_age_train & phone_brand_device_model  to train_phone
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

##1、性别特征 Gender：

```
#train : gender
x=train_phone.gender.value_counts()
print x
p=train_phone.gender.value_counts().plot(kind='bar',figsize=(15,6),rot=0)
_=p.set_xlabel('Gender'),p.set_ylabel('Count')
plt.show()
```

![test pic](/pic/basic1.png)


##2、年龄特征 Age
```
x=train_phone1.ix[train_phone1.gender=='F','group'].value_counts().sort_index()
x1=x/sum(x)
print x1
p=x1.plot(kind='bar',figsize=(15,6),rot=0)
_=p.set_xlabel('Group'),p.set_ylabel('Ratio')
plt.title('Female Age Distribution')
plt.show()


x=train_phone1.ix[train_phone1.gender=='M','group'].value_counts().sort_index()
x1=x/sum(x)
print x1
p=x1.plot(kind='bar',figsize=(15,6),rot=0)
_=p.set_xlabel('Group'),p.set_ylabel('Ratio')
plt.title('Male Age Distribution')
plt.show()

```


![test pic](/pic/female_age.png)

![test pic](/pic/male_age.png)


##3、群组特征 Group:
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


##4、手机品牌特征 Phone_brand：

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




##5、Phone_brand vs Group

将使用次数排序不在前十的手机品牌分组为‘Others’

```
##change the left phone brands except the first 10 to 'else' class
train_phone1=train_phone.copy(deep=True)
name=phone_brand_counts_prop1.index[0:10]
train_phone1.ix[train_phone1.phone_brand.isin(name)==False,'phone_brand']='Others'
print train_phone1.ix[0:5,:]
```
![test pic](/pic/train_phone1.png)


可以看每一个用户分组中，手机品牌使用占比情况：
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

可以看每一个品牌下，不同用户群的占比：
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

##6、Phone_brand vs gender

不同品牌的性别比重
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

不同性别下 ，各个品牌的比重
```
## Phone_brand VS Gender
name1=list(name)
name1.append("Others")##将前十名以后的手机品牌设为‘Others’
data =train_phone1.groupby(["gender", "phone_brand"]).count()["device_id"].unstack().copy(deep = True)
data1=pd.DataFrame(data,columns=name1)
x= data1.div(data1.sum(axis = 1), axis = 0)
print data1
print x
p=x.plot.barh(stacked = True, rot = 1, figsize = (12, 8), width = .4)
_ = p.set_xticklabels(""), p.legend(fontsize =10., loc = "upper center", ncol = 6, borderpad = -.15)
a_ = p.set_ylabel("Gender"), p.set_xlabel("proportion of phone brands")
plt.show()
```
计数

![test pic](/pic/gender_phonebrand.png)

比重

![test pic](/pic/gender_phonebrand_prop.png)

条形图

![test pic](/pic/gender_phonebrand1.png)

PS：视觉上看男女在使用的手机品牌分布上差异不大
这个和我之前在论坛看到的别人的结论不太一样，有可能我过程有问题，请大牛帮我看一下~~

来，吃两块饼：
```
name1 = list(name)
name1.append("Others")
data = train_phone1.groupby(["gender", "phone_brand"]).count()["device_id"].unstack().copy(deep=True)
data1 = pd.DataFrame(data, columns=name1)
x = data1.div(data1.sum(axis=1), axis=0)

female_data = np.array(data1.ix['F', :])
colors=['pink','coral','blue','orange','green']
p = plt.pie(female_data, labels=name1, colors=colors,autopct='%1.1f%%')
plt.title('Phone brands used by Female')
plt.show()

male_data = np.array(data1.ix['M', :])
colors=['pink','coral','blue','orange','green']
p = plt.pie(male_data, labels=name1, colors=colors,autopct='%1.1f%%')
plt.title('Phone brands used by Male')
plt.show()
```

![test pic](/pic/pie_phone_brand_female.png)
![test pic](/pic/pie_phone_brand_male.png)

也可证明 但从Gender 和phone_brand上看，男女差异不大。后续加上年龄，可能会有差异~



##7、Age vs Gender vs Phone_brand

```
##
train_phone1_female=train_phone1.ix[train_phone1.gender=='F',:]
train_phone1_male=train_phone1.ix[train_phone1.gender=='M',:]

data =train_phone1_female.groupby(["phone_brand", "group"]).count()["device_id"].unstack().copy(deep = True)
print data
x=data.div(data.sum(axis=1),axis=0)
p=x.plot.bar(stacked = False, rot = 0, figsize = (15, 8), width = .5)
_ = p.legend(fontsize = 12., loc = "upper right", ncol = 6, borderpad = -.15)
a_ = p.set_ylabel("Count"), p.set_xlabel("Phone_brand")
plt.title('Female Age Distribution on Each Phone Brands')
plt.show()

data =train_phone1_male.groupby(["phone_brand", "group"]).count()["device_id"].unstack().copy(deep = True)
print data
x=data.div(data.sum(axis=1),axis=0)
p=x.plot.bar(stacked = False, rot = 0, figsize = (15, 8), width = .5)
_ = p.legend(fontsize = 12., loc = "upper right", ncol = 6, borderpad = -.15)
a_ = p.set_ylabel("Count"), p.set_xlabel("Phone_brand")
plt.title('male Age Distribution on Each Phone Brands')
plt.show()
```

![test pic](/pic/female_age_distribution_on_phone_brands.png)

![test pic](/pic/male_age_distribution_on_phone_brands.png)

```
data =train_phone1_female.groupby(["group", "phone_brand"]).count()["device_id"].unstack().copy(deep = True)
print data
x=data.div(data.sum(axis=1),axis=0)
p=x.plot.bar(stacked = False, rot = 0, figsize = (15, 8), width = .5)
_ = p.legend(fontsize = 12., loc = "upper right", ncol = 6, borderpad = -.15)
a_ = p.set_ylabel("Count"), p.set_xlabel("Female Age Group")
plt.title('Distribution of Phone Brands on each Female Age Group')
plt.show()

data =train_phone1_male.groupby(["group", "phone_brand"]).count()["device_id"].unstack().copy(deep = True)
print data
x=data.div(data.sum(axis=1),axis=0)
p=x.plot.bar(stacked = False, rot = 0, figsize = (15, 8), width = .5)
_ = p.legend(fontsize = 12., loc = "upper right", ncol = 6, borderpad = -.15)
a_ = p.set_ylabel("Count"), p.set_xlabel("Male Age Group")
plt.title('Distribution of Phone Brands on each Male Age Group')
plt.show()

```

![test pic](/pic/female_phone_brand_age.png)

![test pic](/pic/male_phone_brand_age.png)

```
data =train_phone1_female.groupby(["group", "phone_brand"]).count()["device_id"].unstack().copy(deep = True)
x=data.div(data.sum(axis=1),axis=0)
x1=x.T
print x
print x1
p=x1.plot.bar(stacked = False, rot = 0, figsize = (15, 8), width = .5)
_ = p.legend(fontsize = 12., loc = "upper center", ncol = 6, borderpad = -.15)
a_ = p.set_ylabel("Ratio"), p.set_xlabel("Phone Brands")
plt.title('Ratio of Female Age Group on Phone Brands')
plt.show()

data =train_phone1_male.groupby(["group", "phone_brand"]).count()["device_id"].unstack().copy(deep = True)
x=data.div(data.sum(axis=1),axis=0)
x1=x.T
print x
print x1
p=x1.plot.bar(stacked = False, rot = 0, figsize = (15, 8), width = .5)
_ = p.legend(fontsize = 12., loc = "upper center", ncol = 6, borderpad = -.15)
a_ = p.set_ylabel("Ratio"), p.set_xlabel("Phone Brands")
plt.title('Ratio of Male Age Group on Phone Brands')
plt.show()

```

![test pic](/pic/female_ratio_age_phone_brand.png)

![test pic](/pic/male_ratio_age_phone_brand.png)
