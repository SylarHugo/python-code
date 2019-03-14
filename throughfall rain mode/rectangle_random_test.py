#epsabs=1.49e-06, epsrel=1.49e-06#精度
import numpy
import scipy.integrate
import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
import csv

#基本参数设置
R = 3#圆半径
B = 1#树冠边界间距
rain = 1.0#林外降雨量
length = 1#长
width = 0.2#宽
H = 15#树冠高度
V_rectangle = length * width * H
step_point = 21#B+R的分割点数,分割段数+1
step_range = range(0, step_point, 1)#生成分割序列
differential = (R + B / 2) / (step_point - 1)#分割段长度
#生成多维数组
def one_zeros(self_x):#一维数组
    return numpy.zeros(self_x)
def two_zeros(self_x, self_y):#二维数组
    return numpy.zeros((self_x, self_y))
def there_zeros(self_x, self_y, self_z):#三维数组
    return numpy.zeros((self_x, self_y, self_z))
#四个树冠的圆心
def center_corwn_input():#四个树冠的圆心
    center_corwn_four = two_zeros(4, 2)
    center_corwn_four[0][0] = 0
    center_corwn_four[0][1] = 0
    center_corwn_four[1][0] = 2 * R + B
    center_corwn_four[1][1] = 0
    center_corwn_four[2][0] = 2 * R + B
    center_corwn_four[2][1] = 2 * R + B
    center_corwn_four[3][0] = 0
    center_corwn_four[3][1] = 2 * R + B
    return center_corwn_four
center_circle = center_corwn_input()#四个树冠的圆心
#第i个树冠函数
def func_crown(tree_num):
    return lambda x, y: H - numpy.sqrt((x-center_circle[tree_num][0]) ** 2 +
                                       (y-center_circle[tree_num][1]) ** 2) * H / R
#第i个树冠的上半圆函数
def func_up_crown(i):
    return lambda x:center_circle[i][1] + numpy.sqrt(9 -(x - center_circle[i][0]) ** 2)#上半圆函数
#第i个树冠的下半圆函数
def func_down_crown(i):
    return lambda x:center_circle[i][1] - numpy.sqrt(9 -(x - center_circle[i][0]) ** 2)#下半圆函数



#生成水槽中心点数组，第一维：某点的穿透雨量、X轴坐标、Y轴坐标，第二维X轴定值的Y轴点集合，第三维X轴的集合
ucs = numpy.zeros((step_point, step_point, 3))#中心点数组：截留量、X、Y坐标
#对水槽中心点数组赋值X、Y坐标
for i in step_range:#对水槽中心点数组赋值X、Y坐标
    for j in step_range:
        ucs[i][j][1] = differential * i
        ucs[i][j][2] = differential * j

rectangle = two_zeros(4, 2)#生成长方形4个点的数组
#赋值：xa,xb,2个ab交点，2个cd焦点和圆左右边界 的X轴坐标集合，8个数，分段积分：7段
def rectangle_intersection_sequence(tree_num, rec_arr):
    r_i_s_get = one_zeros(8)
    r_i_s_get[0] = rec_arr[0][0]#长方形xa
    r_i_s_get[1] = rec_arr[1][0]#长方形xb
    r_i_s_get[2] = rec_arr[0][0]  # 长方形ab的第一个交点
    r_i_s_get[3] = rec_arr[0][0]  # 长方形ab的第二个交点
    r_i_s_get[4] = rec_arr[0][0]  # 长方形cd的第一个交点
    r_i_s_get[5] = rec_arr[0][0]  # 长方形cd的第二个交点
    r_i_s_get[6] = center_circle[tree_num][0] - R#树冠左边界
    r_i_s_get[7] = center_circle[tree_num][0] + R#树冠右边界
    #ab与树冠圆心距离的绝对值
    y_ab = abs(center_circle[tree_num][1] - rec_arr[0][1])
    #cd与树冠圆心距离的绝对值
    y_cd = abs(center_circle[tree_num][1] - rec_arr[3][1])
    if y_ab < R:
        # 长方形ab的第一个交点
        r_i_s_get[2] = center_circle[tree_num][0] - numpy.sqrt(R ** 2 - y_ab ** 2)
        # 长方形ab的第二个交点
        r_i_s_get[3] = center_circle[tree_num][0] + numpy.sqrt(R ** 2 - y_ab ** 2)
    if y_cd < R:
        # 长方形cd的第一个交点
        r_i_s_get[4] = center_circle[tree_num][0] - numpy.sqrt(R ** 2 - y_cd ** 2)
        # 长方形cd的第二个交点
        r_i_s_get[5] = center_circle[tree_num][0] + numpy.sqrt(R ** 2 - y_cd ** 2)

    return sorted(r_i_s_get)


#对各长方形4个点赋值，并求与4个树冠相交部分的截留量
for point_one in ucs:#第三维
    for point_two in point_one:#第二维
        rectangle[0][0] = point_two[1] - width/2#xa
        rectangle[0][1] = point_two[2] - length / 2#ya
        rectangle[1][0] = point_two[1] + width / 2#xb
        rectangle[1][1] = point_two[2] - length / 2#yb
        rectangle[2][0] = point_two[1] + width / 2#xc
        rectangle[2][1] = point_two[2] + length / 2#yc
        rectangle[3][0] = point_two[1] - width / 2#xd
        rectangle[3][1] = point_two[2] + length / 2#yd
        #4个树冠的截留量
        rain_interception = one_zeros(4)

        #xa,xb,2个ab交点，2个cd焦点，R的集合，分段积分-6段
        for tree_num in range(0, 4, 1):
            #第i个树冠的分段截留量
            rain_i = one_zeros(7)
            #交点赋值
            r_i_s = rectangle_intersection_sequence(tree_num, rectangle)
            left_limit = max(rectangle[0][0], center_circle[tree_num][0] - R)
            right_limit = min(rectangle[1][0], center_circle[tree_num][0] + R)
            for i in range(0, 7, 1):
                if left_limit <= r_i_s[i] < r_i_s[i+1] <= right_limit:
                    avg_down_crown = (func_down_crown(tree_num)(r_i_s[i]) + func_down_crown(tree_num)(r_i_s[i+1])) / 2
                    avg_up_crown = (func_up_crown(tree_num)(r_i_s[i]) + func_up_crown(tree_num)(r_i_s[i+1])) / 2
                    if avg_down_crown >rectangle[3][1] or avg_up_crown < rectangle[0][1]:
                        continue
                    if avg_down_crown > rectangle[0][1]:
                        func_g = func_down_crown(tree_num)
                    else:
                        func_g = rectangle[0][1]
                    if avg_up_crown < rectangle[3][1]:
                        func_h = func_up_crown(tree_num)
                    else:
                        func_h = rectangle[3][1]
                    rain_i[i] = scipy.integrate.dblquad(func_crown(tree_num), r_i_s[i], r_i_s[i+1], func_g, func_h,
                                                        epsabs=1.49e-06, epsrel=1.49e-06)[0]
            rain_interception[tree_num] = numpy.sum(numpy.abs(rain_i))
        point_two[0] = 100 * (V_rectangle - numpy.sum(rain_interception))/V_rectangle


#生成X,Y的集合
ucs_x = numpy.linspace(0, R + B / 2, step_point)
ucs_y = numpy.linspace(0, R + B / 2, step_point)
UX, UY = numpy.meshgrid(ucs_x, ucs_y)

#生成穿透雨量的二维矩阵，并赋值
ucs_rain = two_zeros(step_point, step_point)
ucs_rain_T = two_zeros(step_point, step_point)
for i in step_range:
    for j in step_range:
        ucs_rain[j][i] = ucs[i][j][0]
        ucs_rain_T[i][j] = ucs[i][j][0]
filesave = r'd:/test.csv'
fs = open(filesave, 'w',encoding='gbk',newline='')
writer = csv.writer(fs)
for record in ucs_rain:
    writer.writerow(record)
fs.close()


fig = matplotlib.pyplot.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.plot_trisurf(UX, UY, ucs_rain, linewidth=0.2, antialiased=True)
ax.plot_wireframe(UX, UY, ucs_rain, rstride=10, cstride=10)
matplotlib.pyplot.show()
b = 2
c = 3

