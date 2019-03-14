#https://blog.csdn.net/helloxiaozhe/article/details/81032718
# coding:utf-8
"""
File Name:  Excel.py
Function:  实现 将计算结果的保存形式由txt转化为excel 的类
Comments:  将计算结果的保存形式由txt转化为excel，从而方便对数据的分析和使用
Author: yyz
Update Time:    2018-06-27 09:57:16
"""
# 系统包
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
# workbook相关
from openpyxl.workbook import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.reader.excel import load_workbook
# 自引包
from Text import Text
class Excel():
    '''Excel相关操作类'''
    def __init__(self):
        self.__in_txt_filename=""
        self.__out_save_excel_filename=""
        self.__head_row_name_list=[u'字段1', u'字段2', u'字段3']
    def __read_excel_with_openpyxl(self, excel_name):
        #读取excel2007文件
        wb = load_workbook(filename=excel_name)
        sheetnames = wb.get_sheet_names()
        ws = wb.get_sheet_by_name(sheetnames[0])
        for row in ws.rows:
            #print "row",row
            for cell in row:
                 print cell.value,
            print ""
 
    # 行标题按行排列
    def __write_to_excel_with_openpyxl_row_head(self,records,save_excel_name,head_row_list):
        from openpyxl import Workbook
        from openpyxl.compat import range
        from openpyxl.utils import get_column_letter
        wb = Workbook()
 
        dest_filename = "row_head_"+save_excel_name.decode('utf-8')
        ws4 = wb.create_sheet(title=str(save_excel_name).decode('utf-8'))
 
        # 写第一行，标题行
        for h_col in range(1, len(head_row_list) + 1):
            # print h_col
            _ = ws4.cell(column=h_col, row=1, value="{0}".format(get_column_letter(h_col))).value = head_row_list[h_col - 1].decode('utf-8')
 
        # 写第二行及其以后的那些行
        row = 2
        for record in records:
            record_list = str(record).strip().split("#$#")
            #print record_list
            for col in range(1, len(record_list) + 1):
                #_ = ws3.cell(column=col, row=row, value="{0}".format(get_column_letter(col)))
                _ = ws4.cell(column=col, row=row, value="{0}".format(get_column_letter(col))).value=record_list[col-1].decode('utf-8')
                #_ = ws4.cell(column=col, row=row).value=record_list[col_index-1].decode('utf-8')
                #print record_list[col-1].decode('utf-8')
 
            row += 1
 
        wb.save(filename=dest_filename)
    # 列标题按照列排列
    def __write_to_excel_with_openpyxl_column_head(self,records,save_excel_name,head_row_list):
        from openpyxl import Workbook
        from openpyxl.compat import range
        from openpyxl.utils import get_column_letter
        wb = Workbook()
 
        dest_filename = "column_head_"+save_excel_name.decode('utf-8')
        ws4 = wb.create_sheet(title=str(save_excel_name).decode('utf-8'))
 
        # 写第一行，标题行
        for h_col in range(1, len(head_row_list) + 1):
            # print h_col
            _ = ws4.cell(column=1, row=h_col, value="{0}".format(get_column_letter(h_col))).value = head_row_list[h_col - 1].decode('utf-8')
 
        # 写第二行及其以后的那些行
        row = 2
        for record in records:
            record_list = str(record).strip().split("#$#")
            #print record_list
            for col in range(1, len(record_list) + 1):
                #_ = ws3.cell(column=col, row=row, value="{0}".format(get_column_letter(col)))
                _ = ws4.cell(column=row, row=col, value="{0}".format(get_column_letter(col))).value=record_list[col-1].decode('utf-8')
                #_ = ws4.cell(column=col, row=row).value=record_list[col_index-1].decode('utf-8')
                #print record_list[col-1].decode('utf-8')
 
            row += 1
 
        wb.save(filename=dest_filename)
 
 
 
 
    '''**********以下是外部可调方法********'''
 
    @classmethod
    def tranform_txt_to_excel(cls, in_txt_filename="in_txt_save_name.txt", in_head_row_name_list=[u'字段1', u'字段2', u'字段3'], out_save_excel_filename="out_excel_save_name.xlsx"):
        '''
        :param in_txt_filename: 
        :param in_head_row_name_list: 
        :param out_save_excel_filename: 
        :return: 
        '''
        dataset=Text.read_from_file(in_filename=in_txt_filename)
        obj_handle_excel = Excel()
        obj_handle_excel.__write_to_excel_with_openpyxl_row_head(dataset, out_save_excel_filename, in_head_row_name_list)
 
        obj_handle_excel.__write_to_excel_with_openpyxl_column_head(dataset, out_save_excel_filename, in_head_row_name_list)
    @classmethod
    def read_excel(cls, in_excel_name="in_excel_name.xlsx"):
        '''
        :param in_excel_name: 
        :return: 
        '''
        if Text.is_file_exists(in_file_name=in_excel_name) is False:
            exit()
        obj_handle_excel = Excel()
        obj_handle_excel.__read_excel_with_openpyxl(excel_name=in_excel_name)
 
if __name__ == '__main__':
    in_txt_filename = "in_txt_save_name.txt"
    in_head_row_name_list = [u'字段1', u'字段2', u'字段3']
    out_save_excel_filename = "out_excel_save_name.xlsx"
    Excel.tranform_txt_to_excel(in_txt_filename, in_head_row_name_list, out_save_excel_filename)
    Excel.read_excel(in_excel_name=out_save_excel_filename)
