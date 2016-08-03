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

#一、用户属性特征

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



#二、用户属性特征 与 手机品牌
```
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

train_test_phone1=pd.read_csv('outputdata/train_test_phone1.csv')
phone_counts=train_test_phone1.phone_brand_en.value_counts()
phone_counts_prop=phone_counts/sum(phone_counts)
phone_counts_prop=np.array(phone_counts_prop)
phone_counts_prop1=pd.Series(np.cumsum(phone_counts_prop),index=phone_counts.index)
name=phone_counts_prop1.index[0:10]
name1=list(name)
name1.append("Others")


train_phone=train_test_phone1.ix[train_test_phone1.label=='train',:]
#train_phone.to_csv('outputdata/train_phone.csv')
#### Group vs phone_brand in Trainning Data
data =train_phone.groupby(["group", "phone_brand_en_class"]).count()["device_id"].unstack().copy(deep = True)
data1=pd.DataFrame(data,columns=name1)
p = data1.div(data.sum(axis = 1), axis = 0).plot.barh(stacked = True, rot = 0, figsize = (15, 8), width = .5)
_ = p.set_xticklabels(""), p.legend(fontsize = 12., loc = "right", ncol = 1, borderpad = -.15)
a_ = p.set_ylabel("Group"), p.set_xlabel("Ratio")
plt.title('Group VS Phone_brand in Training Data')


#### phone_brand vs Group in Trainning Data
data =train_phone.groupby(["phone_brand_en_class", "group"]).count()["device_id"].unstack().copy(deep = True)
data1=pd.DataFrame(data,index=name1)
p = data1.div(data.sum(axis = 1), axis = 0).plot.barh(stacked = True, rot = 0, figsize = (15, 8), width = .5)
_1 = p.set_xticklabels(""), p.legend(fontsize = 10., loc = "lower right", ncol = 1, borderpad = -.15)
a_1= p.set_ylabel("Phone_brand"), p.set_xlabel("Ratio")
plt.title('Phone_brand VS Group in Training Data')

####phone_brand vs Gender in Trainning Data
data =train_phone.groupby(["phone_brand_en_class", "gender"]).count()["device_id"].unstack().copy(deep = True)
data1=pd.DataFrame(data,index=name1)
p = data1.div(data.sum(axis = 1), axis = 0).plot.barh(stacked = True, rot = 0, figsize = (15, 8), width = .5)
_2 = p.set_xticklabels(""), p.legend(fontsize = 20., loc = "upper right", ncol = 1, borderpad = -.15)
a_2= p.set_ylabel("Phone_brand"), p.set_xlabel("Ratio")
plt.title('Phone_brand VS Gender in Training Data')

####Gender vs Phone_brand in Trainning Data
data =train_phone.groupby(["gender", "phone_brand_en_class"]).count()["device_id"].unstack().copy(deep = True)
data1=pd.DataFrame(data,columns=name1)
p = data1.div(data.sum(axis = 1), axis = 0).plot.barh(stacked = True, rot = 0, figsize = (15, 8), width = .5)
_3= p.set_xticklabels(""), p.legend(fontsize = 10., loc = "right", ncol = 1, borderpad = -.15)
a_3= p.set_ylabel("Gender"), p.set_xlabel("Ratio")
plt.title('Gender VS Phone_brand in Training Data')


####Pie plot :Gender vs Phone_brand in Training Data
data =train_phone.groupby(["gender", "phone_brand_en_class"]).count()["device_id"].unstack().copy(deep = True)
data1=pd.DataFrame(data,columns=name1)
x = data1.div(data1.sum(axis=1), axis=0)
female_data = np.array(data1.ix['F', :])
colors=['pink','coral','blue','orange','green']
p1= plt.pie(female_data, labels=name1, colors=colors,autopct='%1.1f%%')
plt.title('Phone brands used by Female')

male_data = np.array(data1.ix['M', :])
colors=['pink','coral','blue','orange','green']
p2= plt.pie(male_data, labels=name1, colors=colors,autopct='%1.1f%%')
plt.title('Phone brands used by Male')



#### barplot: Gender_Phone_brand_Age
train_phone_female=train_phone.ix[train_phone.gender=='F',:]
train_phone_male=train_phone.ix[train_phone.gender=='M',:]

data =train_phone_female.groupby(["phone_brand_en_class", "group"]).count()["device_id"].unstack().copy(deep = True)
print data
x1=pd.DataFrame(data,index=name1)
p3=x1.plot.bar(stacked = False, rot = 0, figsize = (15, 8), width = .5)
_p3 = p3.legend(fontsize = 12., loc = "upper right", ncol = 6, borderpad = -.15)
a_p3 = p3.set_ylabel("Count"), p.set_xlabel("Phone_brand")
plt.title('Female Age Distribution on Each Phone Brands')


data =train_phone_male.groupby(["phone_brand_en_class", "group"]).count()["device_id"].unstack().copy(deep = True)
x1=pd.DataFrame(data,index=name1)
p4=x1.plot.bar(stacked = False, rot = 0, figsize = (15, 8), width = .5)
_p4 = p4.legend(fontsize = 12., loc = "upper right", ncol = 6, borderpad = -.15)
a_p4 = p4.set_ylabel("Count"), p.set_xlabel("Phone_brand")
plt.title('Male Age Distribution on Each Phone Brands')
plt.show()

```
![test pic](/pic/Phonebrand_group_train.png)

![test pic](/pic/Group_Phonebrand_train.png)

![test pic](/pic/Phonebrand_gender_train.png)

![test pic](/pic/Gender_phonebrand_train.png)

![test pic](/pic/pie_Phonebrand_gender_train.png)

![test pic](/pic/pie_Phonebrand_gender_test.png)

![test pic](/pic/Female_Phonebrand_Age_train.png)

![test pic](/pic/Male_Phonebrand_Age_train.png)
