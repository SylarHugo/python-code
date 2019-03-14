#unit: square dm
#epsabs=1.49e-06, epsrel=1.49e-06#精度
import mode_rectangle
import mode_square
import mode_circle
import numpy
import math
import scipy.integrate
import matplotlib.pyplot
import csv
import time
b_time = time.time()
file_save = r'd:/test.csv'
#初始值initial value，cannot_accpet容差范围%
H, R, B, pi, step_point, canot_accept = [150, 30, 10, math.pi, 36, 5]
#模型基础参数
mode_side = R + B / 2#样地边长
mode_S = pow(mode_side, 2)#样地面积
V_s = mode_S * H#样地体积
R2 = pow(R, 2)
V_canopy = pi * R2 * H / 12#树冠体积
V_throughfall = V_s - V_canopy#穿透雨体积
R_t = V_throughfall / mode_S#模型区域穿透雨值
accept_ratio = [R_t * (100 - canot_accept) / 100, R_t * (100 + canot_accept) / 100]#水槽测的穿透雨的容差范围值
#模型初始值设置
S_f = numpy.arange(10, 101, 5)#水槽面积 单位平方分米
ratio_l_w = numpy.arange(2, 23, 4)#长宽比
len_S_f = len(S_f)#模型面积范围举例个数
len_ratio_l_w = len(ratio_l_w)#长宽比数组举例素个数
circle_accept_point_num = numpy.zeros(len_S_f)#不同面积，圆合适点个数
square_accept_point_num = numpy.zeros(len_S_f)#不同面积，正方形合适点个数
rectangle_accept_point_num = numpy.zeros(len_S_f)#不同面积，长方形合适点个数
rectanle_accept_ratio = numpy.zeros(len_S_f)#不同面积，的长款比（最佳长宽比）
len_s = 0#面积模型数组的排序
for square_dm in S_f:
    radius = numpy.sqrt(square_dm / pi)#圆的半径
    initial_value = [R, B, H, square_dm, radius, step_point, accept_ratio[0], accept_ratio[1]]
    circle_accept_point_num[len_s] = mode_circle.m_c(initial_value)#圆形水槽：采集穿透雨 >= 95% 全林穿透雨占比的个数
    s_length = numpy.sqrt(square_dm)#正方形边长
    initial_value = [R, B, H, square_dm, s_length, step_point, accept_ratio[0], accept_ratio[1]]
    square_accept_point_num[len_s] = mode_square.m_s(initial_value)
    #长方形
    len_r = 0
    rectangle_best_S_point = numpy.zeros(len_S_f)  # 等面积长方形，合适点个数
    rectangle_best_ratio = numpy.zeros(len_S_f)  # 等面积长方形，合适点的长宽比
    for len_l_w in ratio_l_w:  # len_rp等面积内，长方形长宽比数组的排序
        r_width = numpy.sqrt(square_dm / len_l_w)
        r_length = r_width * len_l_w
        initial_value = [R, B, H, square_dm, r_length, r_width, step_point, accept_ratio[0], accept_ratio[1]]
        rectangle_best_S_point[len_r] = mode_rectangle.m_r(initial_value)  # 满足接受条件的点的个数
        if len_r == 0:
            rectangle_accept_point_num[len_s] = rectangle_best_S_point[len_r]
            rectanle_accept_ratio[len_s] = len_l_w
        elif rectangle_best_S_point[len_r] > rectangle_accept_point_num[len_s]:
            rectangle_accept_point_num[len_s] = rectangle_best_S_point[len_r]
            rectanle_accept_ratio[len_s] = len_l_w
        len_r = len_r + 1
    len_s = len_s + 1
csv_arr = numpy.vstack((S_f, circle_accept_point_num, square_accept_point_num, rectangle_accept_point_num,
                        rectanle_accept_ratio)).T
fs = open(file_save, 'w', encoding='gbk', newline='')
writer = csv.writer(fs)
for j in csv_arr:
    writer.writerow(j)
fs.close()
e_time = time.time()
print(e_time - b_time)