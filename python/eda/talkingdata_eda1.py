# coding = utf-8
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
gender_age_train=pd.read_csv('kaggledata/gender_age_train.csv')
gender_age_test=pd.read_csv('kaggledata/gender_age_test.csv')
phone_brand_device_model=pd.read_csv('kaggledata/phone_brand_device_model.csv')
events=pd.read_csv('kaggledata/events.csv')
#app_events=pd.read_csv('kaggledata/app_events.csv')
app_labels=pd.read_csv('kaggledata/app_labels.csv')
train_test=pd.concat([gender_age_train,gender_age_test],ignore_index=True)


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

#phone_brand
phone_brand_counts=train_phone.phone_brand.value_counts()
phone_brand_counts_prop=phone_brand_counts/sum(phone_brand_counts)
phone_brand_counts_prop=np.array(phone_brand_counts_prop)
phone_brand_counts_prop1=pd.Series(np.cumsum(phone_brand_counts_prop),index=phone_brand_counts.index)


##change the left phone brands except the first 10 to 'Oher' class
train_phone1=train_phone.copy(deep=True)
name=phone_brand_counts_prop1.index[0:10]
print name
train_phone1.ix[train_phone1.phone_brand.isin(name)==False,'phone_brand']='Others'



print '............................'
## Phone_brand VS Gender
data =train_phone1.groupby(["gender", "phone_brand"]).count()["device_id"].unstack().copy(deep = True)
x= data.div(data.sum(axis = 1), axis = 0)
print x
name1=list(name)
name1.append("Others")
x1=pd.DataFrame(x,columns=name1)
print x1
p=x1.plot.barh(stacked = True, rot = 0, figsize = (15, 8), width = .5)
_ = p.set_xticklabels(""), p.legend(fontsize =20., loc = "right", ncol = 1, borderpad = -.15)
a_ = p.set_ylabel("Gender"), p.set_xlabel("Count")
plt.show()



























