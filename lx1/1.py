import numpy
a = numpy.zeros([2,3])
n=1
for i in [0,1]:
    for j in [0,1,2]:
        a[i,j]=a[i,j]+n
        n+=1
print(a)
13