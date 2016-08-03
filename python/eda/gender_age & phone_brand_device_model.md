#用户属性特征 与 手机品牌
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
![test pic1](/python/eda/pic1/Phonebrand_group_train.png)

![test pic1](/python/eda/pic1/Group_Phonebrand_train.png)

![test pic1](/python/eda/pic1/Phonebrand_gender_train.png)

![test pic1](/python/eda/pic1/Gender_phonebrand_train.png)

![test pic1](/python/eda/pic1/pie_Phonebrand_gender_train.png)

![test pic1](/python/eda/pic1/pie_Phonebrand_male_train.png)

![test pic1](/python/eda/pic1/Female_Phonebrand_Age_train.png)

![test pic1](/python/eda/pic1/Male_Phonebrand_Age_train.png)

![test pic1](/python/eda/pic1/Female_Age_Phonebrand_train.png)

![test pic1](/python/eda/pic1/Male_Age_Phonebrand_train.png)