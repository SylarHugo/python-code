import numpy
import pandas


path=r'D:\Ecological Station\DATA\Reported data\vba\2019\national forestry 2019 Stemflow.xlsx'
paths=r'D:\Ecological Station\DATA\Reported data\vba\2019\national forestry 2019 Stemflows.xlsx'
date=pandas.date_range(start='20190101',end='20190104',freq='D',closed='left')
df=pandas.read_excel(path,sheet_name=0,nrows=1)
df=pandas.read_excel(path,sheet_name=0,names=range(1,df.shape[1]+1))


writer=pandas.ExcelWriter(paths)
df.to_excel(excel_writer=writer,sheet_name='2018')
writer.save()
writer.colse()

