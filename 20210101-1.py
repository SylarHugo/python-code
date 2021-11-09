import pandas
import os
#按金额和备注中第几个字 查找
path = r'G:\qqq'
f = os.listdir(path)
f11 = os.path.join(path,f[0])
fzj = os.path.join(path,f[2])
fzz = os.path.join(path,f[3])
d11 = pandas.read_excel(f11,sheet_name = 0, header = None, names = range(0,11))
dzj = pandas.read_excel(fzj,sheet_name = 0, header = None, names = range(0,11))

d11 = d11.fillna('nan')
dzj = dzj.fillna('nan')
d116 = d11[6]
dzj6 = dzj[6]
d11.drop(10,axis=1,inplace = True)
dzj.drop(10,axis=1,inplace = True)
d11.drop(6,axis=1,inplace = True)
dzj.drop(6,axis=1,inplace = True)
r11, c11 = d11.shape
rzj, czj = dzj.shape
row11 = d11.index
rowzj = dzj.index
col1z = dzj.columns
def f2m2b3(str11,strzj):
    str11_f2 = str11[:2]
    strzj_f2 = strzj[:2]
#    str11_m2 = str11[2:4]
#    strzj_m2 = strzj[2:4]
    str11_b3 = str11[-3:]
    strzj_b3 = strzj[-3:]
    if str11_f2 == strzj_f2 and str11_b3 == strzj_b3:
        bol = 1
    else:
        bol = 0
    return bol
l11 = []
lzj = []
h11 = []
hzj = []

for n11 in row11:
    for nzj in rowzj:
        if nzj in hzj:
            continue
        tof = d11.loc[n11,col1z] == dzj.loc[nzj,col1z]
#        if n11 == 1 and  nzj == 1:
#           print(tof)
#            print(d11.loc[1])
#            print(tof)
#            print(tof)

        if all (x for x in tof):
            bol = f2m2b3(d116[n11],dzj6[nzj])
            if bol :
                h11.append(n11)
                hzj.append(nzj)
                break
            else:
                bol = 0
                continue
        else:
            continue

for i in row11:
    if i not in h11:
        l11.append(i)
    
for i in rowzj:
    if i not in hzj:
        lzj.append(i)
d11 = pandas.read_excel(f11,sheet_name = 0, header = None, names = range(0,11))
dzj = pandas.read_excel(fzj,sheet_name = 0, header = None, names = range(0,11))
dfh11 = d11.loc[d11.index.isin(h11)]
dfhzj = dzj.loc[dzj.index.isin(hzj)]
dfl11 = d11.loc[d11.index.isin(l11)]
dflzj = dzj.loc[dzj.index.isin(lzj)]
print('sec')
writer = pandas.ExcelWriter(fzz, mode='a', engine='openpyxl') # pylint: disable=abstract-class-instantiated
dfh11.to_excel(writer, sheet_name = 'dfh11')
dfhzj.to_excel(writer, sheet_name = 'dfhzj')
dfl11.to_excel(writer, sheet_name = 'dfl11')
dflzj.to_excel(writer, sheet_name = 'dflzj')
writer.save()
writer.close()
print('sec')
