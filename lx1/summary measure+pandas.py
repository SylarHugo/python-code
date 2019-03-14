#https://blog.csdn.net/A632189007/article/details/76176985

import numpy as np
import pandas as pd

np.random.seed(1234)
d1 = pd.Series(2*np.random.normal(size = 100)+3)
d2 = np.random.f(2,4,size = 100)
d3 = np.random.randint(1,100,size = 100)

d1.count()          #非空元素计算
d1.min()            #最小值
d1.max()            #最大值
d1.idxmin()         #最小值的位置，类似于R中的which.min函数
d1.idxmax()         #最大值的位置，类似于R中的which.max函数
d1.quantile(0.1)    #10%分位数
d1.sum()            #求和
d1.mean()           #均值
d1.median()         #中位数
d1.mode()           #众数
d1.var()            #方差
d1.std()            #标准差
d1.mad()            #平均绝对偏差
d1.skew()           #偏度
d1.kurt()           #峰度
d1.describe()       #一次性输出多个描述性统计指标

def status(x) : 
    return pd.Series([x.count(),x.min(),x.idxmin(),x.quantile(.25),x.median(),
                      x.quantile(.75),x.mean(),x.max(),x.idxmax(),x.mad(),x.var(),
                      x.std(),x.skew(),x.kurt()],index=['总数','最小值','最小值位置','25%分位数',
                    '中位数','75%分位数','均值','最大值','最大值位数','平均绝对偏差','方差','标准差','偏度','峰度'])

df = pd.DataFrame(status(d1))
df


df = pd.DataFrame(np.array([d1,d2,d3]).T, columns=['x1','x2','x3'])
df.head()

df.apply(status)

加载CSV数据

import numpy as np
import pandas as pd

bank = pd.read_csv("D://bank/bank-additional-train.csv")
bank.head()    #查看前5行

描述性统计1：describe()
result = bank['age'].describe()
pd.DataFrame(result )   #格式化成DataFrame
描述性统计2：describe(include=[‘number’])
include中填写的是数据类型，若想查看所有数据的统计数据，则可填写object，即include=['object']；若想查看float类型的数据，则为include=['float']。
result = bank.describe(include=['object'])
bank.describe(include=['number'])
连续变量的相关系数（corr）
bank.corr()
协方差矩阵（cov）
bank.cov()
删除列
bank.drop('job', axis=1)    #删除年龄列，axis=1必不可少
排序
bank.sort_values(by=['job','age'])  #根据工作、年龄升序排序
bank.sort_values(by=['job','age'], ascending=False)     #根据工作、年龄降序排序
多表连接
准备数据
import numpy as np
import pandas as pd

student = {'Name':['Bob','Alice','Carol','Henry','Judy','Robert','William'],
           'Age':[12,16,13,11,14,15,24],
           'Sex':['M','F','M','M','F','M','F']}

score = {'Name':['Bob','Alice','Carol','Henry','William'],
         'Score':[75,35,87,86,57]}

df_student = pd.DataFrame(student)
df_student

df_score = pd.DataFrame(score)
df_score
内连接
stu_score1 = pd.merge(df_student, df_score, on='Name')
stu_score1
左连接
tu_score2 = pd.merge(df_student, df_score, on='Name',how='left')
stu_score2
查询某一字段数据为空的数量
sum(pd.isnull(stu_score2['Score']))
结果：2
直接删除缺失值
stu_score2.dropna()
删除所有行为缺失值的数据
import numpy as np
import pandas as pd

df = pd.DataFrame([[1,2,3],[3,4,np.nan],
                  [12,23,43],[55,np.nan,10],
                  [np.nan,np.nan,np.nan],[np.nan,1,2]],
                  columns=['a1','a2','a3'])
df.dropna()     #该操作会删除所有有缺失值的行数据
df.dropna(how='all')    #该操作仅会删除所有列均为缺失值的行数据
填充数据
用0填补所有缺失值
df.fillna(0)
采用前项填充或后向填充
df.fillna(method='ffill')   #用前一个值填充
df.fillna(method='bfill')   #用后一个值填充
使用常量填充不同的列
df.fillna({'a1':100,'a2':200,'a3':300})
用均值或中位数填充各自的列
a1_median = df['a1'].median()   #计算a1列的中位数
a1_median=7.5

a2_mean = df['a2'].mean()       #计算a2列的均值
a2_mean = 7.5

a3_mean = df['a3'].mean()       #计算a3列的均值
a3_mean = 14.5

df.fillna({'a1':a1_median,'a2':a2_mean,'a3':a3_mean})   #填充值
数据打乱（shuffle）
df = df.sample(frac=1)
df = df.sample(frac=1).reset_index(drop=True)








