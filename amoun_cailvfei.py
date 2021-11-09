import pandas
import numpy
#按金额和备注是否含有某些字 查找
pathd = r'C:\Users\sylar\Desktop\abc.xlsx'
path1 = r'C:\Users\sylar\Desktop\f1.xlsx'
path2 = r'C:\Users\sylar\Desktop\f2.xlsx'
path3 = r'C:\Users\sylar\Desktop\f3.xlsx'

f1 = pandas.read_excel(pathd,sheet_name= 'Sheet1')
f2 = pandas.read_excel(pathd,sheet_name='Sheet2')
f1['sn1'] = f1.index + 1
f2['sn2'] = f2.index + 1

listcol1 = f1.columns
listcol2 = f2.columns

f3=f1.loc[0:1,listcol1]
for i in listcol2:
    f3[i]=f2[i]
for i in f3.columns:
    for j in [0,1]:
        f3.loc[j,i] = numpy.nan
f3['sn'] = f3.index + 1

k = 0
for i in f1.index:
    str1 = f1.loc[i, 'name1']
    str3 = f1.loc[i, 'payment note1']
    if str3 is numpy.nan or str1 is numpy.nan:
        continue
    str = '人工费'
    str_1 = '地租费'
    str_2 = '租地费'
    str_3 = '苗木'
    if str3.find(str) >= 0:
        ll = list(f2[f2['amoun2'] == f1.loc[i, 'amoun1']]['sn2'])
        if len(ll) == 0:
            continue
        for jj in ll:
            j = jj - 1
            str2 = f2.loc[j, 'payment note2']
            if str2.find(str1) > 0:#找名字
                #if str2.find(str) > 0:#差路费
                if str2.find(str) or str2.find(str_1) > 0 or str2.find(str_2) or str2.find(str_3):#人工费
                    f3.loc[k, listcol1] = f1.loc[i, listcol1]
                    f3.loc[k, listcol2] = f2.loc[j, listcol2]
                    f1.loc[i, listcol1] = None
                    f2.loc[j, listcol2] = None
                    k = k + 1
                    break
f1.to_excel(path1)
f2.to_excel(path2)
f3.to_excel(path3)
del(f1, f2, f3)
