import numpy as np
a=np.array([1,2,3,4,5,6,7,8,9]) # sorted 之后的结果
num=len(a)
N=num-1
print(N)#N个区间
# 计算百分位数
P=10 # 百分位数
floor1=int(np.floor(N/100*P))#下限 
'''floor1=np.floor(N/100*P) foolr1=floor1 if floor1==(N/100*P) else floor1-1 floor1=int(floor1) '''
ceil1=int(np.ceil(N/100*P))#上限
if floor1==ceil1:
    floor1-=1
#所在区间 a[floor1] - a[ceil1]
P_n=a[floor1]+(a[ceil1]-a[floor1])*(N/100*P-floor1) # also np.percentile(a,10)
print(P_n)

b=np.array([1,1,2,3,4,5,6,7,8,9])# sorted 之后的结果
num=len(b)
N=num-1
print(N)
# 计算百分位数
P=10 # 百分位数
floor1=int(np.floor(N/100*P))
ceil1=int(np.ceil(N/100*P))
if floor1==ceil1:
    floor1-=1
#所在区间 a[floor1] - a[ceil1]
P_n=b[floor1]+(b[ceil1]-b[floor1])*(N/100*P-floor1)# also np.percentile(b,10)
print(P_n)
