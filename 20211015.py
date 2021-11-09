import pandas as pd
#按金额、是否含有备注字查找
path1 = r'C:\Users\sylar\Desktop\1.xlsx'
path2 = r'C:\Users\sylar\Desktop\2.xlsx'
path10 = r'C:\Users\sylar\Desktop\10.xlsx'
path20 = r'C:\Users\sylar\Desktop\20.xlsx'
path11 = r'C:\Users\sylar\Desktop\11.xlsx'
path21 = r'C:\Users\sylar\Desktop\21.xlsx'
df1 = pd.read_excel(path1)
df2 = pd.read_excel(path2)
delrn = ['月初','本月','本年']
dr=[]
for i in range(851):
    for j in delrn:
        if j in df1['zy'][i]:
            dr.append(i)
            break
df1.drop(labels =dr,inplace = True)
index1=df1.index
index2=df2.index
dr1 = []
dr2 = []
for i in index1:
    for j in index2:
        if df2['金额'][j] == df1['d'][i] and df2['收款人名称'][j] in df1['zy'][i] and j not in dr2:
                dr1.append(i)
                dr2.append(j)
                break 
df1.loc[dr1].to_excel(path10)
df2.loc[dr2].to_excel(path20)
df1.drop(labels =dr1,inplace = True)
df2.drop(labels =dr2,inplace = True)
df1.to_excel(path11)
df2.to_excel(path21)


