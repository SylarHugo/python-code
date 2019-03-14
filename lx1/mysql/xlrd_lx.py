import xlrd
workbook = xlrd.open_workbook(r'D:\python\mysql\lxxlsx.xlsx')
w1=workbook.sheet_by_index(0)
a=w1.col_slice(1,start_rowx=0,end_rowx=6)
b=w1.col_types(1,start_rowx=0,end_rowx=6)

import os
os.system("D:\python\mysql\121.py")
