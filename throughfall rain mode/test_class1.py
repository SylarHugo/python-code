#epsabs=1.49e-06, epsrel=1.49e-06#精度
import numpy
import scipy.integrate
import math
import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
import csv
#initial_value：冠幅，间距，冠高，面积，宽，长，分段个数，R,B,H,square_dm, r_length,r_width, step_point, percentage

accept_p = numpy.zeros(2)
#基本参数设置
pi = math.pi
initial_value = [30, 10, 150, 100, 2, 25, 36, 0, 0]
R, B, H, S, length, width, step_point, accept_p[0], accept_p[1] = initial_value
hegyi_ratio = pow(2, 0.5)#扩展比例
V_s = S * H#穿透雨的立方形体积
R2 = pow(R, 2)
step_range = range(0, step_point, 1)#生成分割序列
mode_limit = (R + B / 2) * hegyi_ratio#路径长
d_limit = mode_limit / (step_point - 1)#路径分割段长度
aa = (pow(mode_limit, 2) - pi * R2 / 12) * H / pow(mode_limit, 2)
accept_p = [aa * 0.95, aa * 1.05]
#四个树冠的圆心
def canopy_center_point():#四个树冠的圆心
    canopy_circle_center = numpy.zeros((4, 2))
    canopy_circle_center[0][0] = 0
    canopy_circle_center[0][1] = 0
    canopy_circle_center[1][0] = mode_limit
    canopy_circle_center[1][1] = -mode_limit
    canopy_circle_center[2][0] = 2 * mode_limit
    canopy_circle_center[2][1] = 0
    canopy_circle_center[3][0] = mode_limit
    canopy_circle_center[3][1] = mode_limit
    return canopy_circle_center
canopy_dot = canopy_center_point()#四个树冠的圆心
#第i个树冠体积函数
def f_canopy(i):#i=tree_num
    return lambda x, y: H - numpy.sqrt((x - canopy_dot[i][0]) ** 2 + (y - canopy_dot[i][1]) ** 2) * H / R
#第i个树冠的上半圆函数
def f_up_canopy(i):#i=tree_num
    return lambda x: canopy_dot[i][1] + numpy.sqrt(R2 - (x - canopy_dot[i][0]) ** 2)#上半圆函数
#第i个树冠的下半圆函数
def func_down_crown(i):#i=tree_num
    return lambda x: canopy_dot[i][1] - numpy.sqrt(R2 - (x - canopy_dot[i][0]) ** 2)#下半圆函数
#生成水槽中心点数组，第一维：某点的穿透雨量、X轴坐标、Y轴坐标，第二维X轴定值的Y轴点集合，第三维X轴的集合
ucs = numpy.zeros((step_point, 3))#中心点数组：截留量、X、Y坐标
#对水槽中心点数组赋值X、Y坐标
for i in step_range:#对水槽中心点数组赋值X、Y坐标
    ucs[i][1] = d_limit * i
    ucs[i][2] = 0
#赋值：xa,xb,2个ab交点，2个cd焦点和圆左右边界 的X轴坐标集合，8个数，分段积分：7段
def intersection_point_sequence(tree, rec_arr):
    r_i_s_get = numpy.zeros(8)
    r_i_s_get[0] = rec_arr[0][0]#长方形xa
    r_i_s_get[1] = rec_arr[1][0]#长方形xb
    r_i_s_get[2] = rec_arr[0][0]  # 长方形ab的第一个交点
    r_i_s_get[3] = rec_arr[0][0]  # 长方形ab的第二个交点
    r_i_s_get[4] = rec_arr[0][0]  # 长方形cd的第一个交点
    r_i_s_get[5] = rec_arr[0][0]  # 长方形cd的第二个交点
    r_i_s_get[6] = canopy_dot[tree][0] - R#树冠左边界
    r_i_s_get[7] = canopy_dot[tree][0] + R#树冠右边界
    #ab与树冠圆心距离的绝对值
    y_ab = abs(canopy_dot[tree][1] - rec_arr[0][1])
    #cd与树冠圆心距离的绝对值
    y_cd = abs(canopy_dot[tree][1] - rec_arr[3][1])
    if y_ab < R:
        # 长方形ab的第一个交点
        r_i_s_get[2] = canopy_dot[tree][0] - numpy.sqrt(R2 - y_ab ** 2)
        # 长方形ab的第二个交点
        r_i_s_get[3] = canopy_dot[tree][0] + numpy.sqrt(R2 - y_ab ** 2)
    if y_cd < R:
        # 长方形cd的第一个交点
        r_i_s_get[4] = canopy_dot[tree][0] - numpy.sqrt(R2 - y_cd ** 2)
        # 长方形cd的第二个交点
        r_i_s_get[5] = canopy_dot[tree][0] + numpy.sqrt(R2 - y_cd ** 2)
    return sorted(r_i_s_get)#排升序
#对各长方形4个点赋值，并求与4个树冠相交部分的截留量
for one_dimensional in ucs:#第二维
    rectangle = numpy.zeros((4, 2))  # 生成长方形4个点的数组
    canopy_interception = numpy.zeros(4)  # 4个树冠的截留量
    rectangle[0][0] = one_dimensional[1] - length / 2#xa
    rectangle[0][1] = one_dimensional[2] - width / 2#ya
    rectangle[1][0] = one_dimensional[1] + length / 2#xb
    rectangle[1][1] = one_dimensional[2] - width / 2#yb
    rectangle[2][0] = one_dimensional[1] + length / 2#xc
    rectangle[2][1] = one_dimensional[2] + width / 2#yc
    rectangle[3][0] = one_dimensional[1] - length / 2#xd
    rectangle[3][1] = one_dimensional[2] + width / 2#yd
    #xa,xb,2个ab交点，2个cd焦点，R的集合，分段积分-6段
    for tree in range(0, 4, 1):
        #第i个树冠的分段截留量
        rain_i = numpy.zeros(7)
        #交点赋值
        r_i_s = intersection_point_sequence(tree, rectangle)
        left_limit = max(rectangle[0][0], canopy_dot[tree][0] - R)
        right_limit = min(rectangle[1][0], canopy_dot[tree][0] + R)
        for i in range(0, 7, 1):
            if left_limit <= r_i_s[i] < r_i_s[i+1] <= right_limit:
                avg_down_crown = (func_down_crown(tree)(r_i_s[i]) + func_down_crown(tree)(r_i_s[i + 1])) / 2
                avg_up_crown = (f_up_canopy(tree)(r_i_s[i]) + f_up_canopy(tree)(r_i_s[i + 1])) / 2
                if avg_down_crown > rectangle[3][1] or avg_up_crown < rectangle[0][1]:
                    continue
                if avg_down_crown > rectangle[0][1]:
                    func_g = func_down_crown(tree)
                else:
                    func_g = rectangle[0][1]
                if avg_up_crown < rectangle[3][1]:
                    func_h = f_up_canopy(tree)
                else:
                    func_h = rectangle[3][1]
                rain_i[i] = scipy.integrate.dblquad(f_canopy(tree), r_i_s[i], r_i_s[i + 1], func_g, func_h,
                                                    epsabs=1.49e-06, epsrel=1.49e-06)[0]
        canopy_interception[tree] = numpy.sum(numpy.abs(rain_i))
    one_dimensional[0] = (V_s - numpy.sum(canopy_interception)) / S
rectangle_p_num = 0
for i in step_range:
    if accept_p[0] < ucs[i][0] < accept_p[1]:
        rectangle_p_num = rectangle_p_num + 1
print(rectangle_p_num)

