import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
##读入数据
app_events=pd.read_csv('kaggledata/app_events.csv')
app_labels=pd.read_csv('kaggledata/app_labels.csv')
events=pd.read_csv('kaggledata/app_labels.csv')
gender_age_test=pd.read_csv('kaggledata/gender_age_test.csv')
gender_age_train=pd.read_csv('kaggledata/gender_age_train.csv')
label_categories=pd.read_csv('kaggledata/label_categories.csv')
phone_brand_device_model=pd.read_csv('kaggledata/phone_brand_device_model.csv')
sample_submission=pd.read_csv('kaggledata/sample_submission.csv')

##去除phone_brand_device_model中重复的行
x1=phone_brand_device_model.drop_duplicates()
x2=x1.duplicated('device_id')
x3=x2[x2==True].index
print x1.ix[x3,:]
m=x1.ix[x3,'device_id']
for i in m:
    print phone_brand_device_model[phone_brand_device_model['device_id'] == i]
    print i

##探索gender/age/group等特征
##merge gender_age_train and phone_brand_device_model as train_phone
train_phone=pd.merge(gender_age_train,phone_brand_device_model_1,on='device_id',how='left')
print train_phone.shape
print train_phone.ix[0:5,:]
#train : gender
x=train_phone.gender.value_counts()
print x
p=train_phone.gender.value_counts().plot(kind='bar',figsize=(15,6),rot=0)
_=p.set_xlabel('Gender'),p.set_ylabel('Count')
plt.show()

#train : age
x=train_phone.age.value_counts().sort_index()
print x
p=train_phone.age.value_counts().plot(kind='bar',figsize=(15,6),rot=0)
_=p.set_xlabel('Age'),p.set_ylabel('Count')
plt.show()

#train : group
x=train_phone.group.value_counts().sort_index()
print x
p=train_phone.group.value_counts().sort_index().plot(kind='bar',figsize=(15,6),rot=0)
_=p.set_xlabel('Group'),p.set_ylabel('Count')
plt.show()
['Xiaomi','Samsung','Huawei','OPPO','Vivo','Meizu','Kupai','Lianxiang','Jinli']
