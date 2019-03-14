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
mode_limit = R + B / 2
R2 = pow(R, 2)
rain_out = pow(mode_limit, 2) * H
canopy_interception = pi * R2 * H / 12
throughfall = rain_out - canopy_interception#林分穿透雨
percentage = throughfall / rain_out#林分穿透雨占比
accept_p = [percentage * (100 - canot_accept), percentage * (100 + canot_accept)]#水槽测的穿透雨的容差范围值
#模型初始值设置
S = numpy.arange(10, 101, 5)#水槽面积 单位平方分米
rate_l_w = numpy.arange(2, 23, 4)#长宽比
S_sum = len(S)#面积模型个数
rate_l_w_sum = len(rate_l_w)#长宽比数组中元素个数
circle_p_num = numpy.zeros(S_sum)#圆percentage，面积
square_p_num = numpy.zeros(S_sum)#正方形percentage，面积
rectangle_p_num = numpy.zeros(S_sum)#长方形percentage，不面积的比例
rectangle_bpr = numpy.zeros(S_sum)#长方形percentage，rate,best,最佳长宽比
rectangle_rp = numpy.zeros(rate_l_w_sum)#同面积不同长宽比的比例rate_l_w,percentage
len_i = 0#面积模型数组的排序
for square_dm in S:
    radius = numpy.sqrt(square_dm / pi)#圆的半径
    initial_value = [R, B, H, square_dm, radius, step_point, accept_p[0], accept_p[1]]
    circle_p_num[len_i] = mode_circle.m_c(initial_value)#圆形水槽：采集穿透雨 >= 95% 全林穿透雨占比的个数
    s_length = numpy.sqrt(square_dm)#正方形边长
    initial_value = [R, B, H, square_dm, s_length, step_point, accept_p[0], accept_p[1]]
    square_p_num[len_i] = mode_square.m_s(initial_value)
    #长方形
    # len_best_rp = 0#等面积内，最佳长宽比的排序位数
    # best_rp = 0#等面积内，最佳长宽比
    # for len_rp in range(0, len(rate_l_w), 1):#len_rp等面积内，长方形长宽比数组的排序
    #     rp = rate_l_w[len_rp]
    #     r_width = numpy.sqrt(square_dm / rp)
    #     r_length = r_width * rp
    #     initial_value = [R, B, H, square_dm, r_length, r_width, step_point, accept_p[0], accept_p[1]]
    #     rectangle_rp[len_rp] = mode_rectangle.m_r(initial_value)#满足接受条件的点的个数
    #     if len_rp == 0:
    #         len_best_rp = len_rp
    #         best_rp = rp
    #     elif rectangle_rp[len_rp] > rectangle_rp[len_rp - 1]:
    #         len_best_rp = len_rp
    #         best_rp = rp
    # rectangle_p_num[len_i] = rectangle_rp[len_best_rp]
    # rectangle_bpr[len_i] = best_rp
    len_i = len_i + 1
csv_arr = numpy.vstack((S, circle_p_num, square_p_num, rectangle_p_num, rectangle_bpr)).T
fs = open(file_save, 'w', encoding='gbk', newline='')
writer = csv.writer(fs)
for j in csv_arr:
    writer.writerow(j)
fs.close()
e_time = time.time()
print(e_time - b_time)

# matplotlib.pyplot.plot(S, circle_p_num, 'r', S, square_p_num, 'b', S, rectangle_p_num, 'b')
# matplotlib.pyplot.savefig('d:/program/photo/different_shapes_throughfull.png')
# matplotlib.pyplot.show()
# matplotlib.pyplot.close()
# matplotlib.pyplot.plot(S, rectangle_bpr)
# matplotlib.pyplot.savefig('d:/program/photo/best_rate_of_percentage.png')
# matplotlib.pyplot.show()
# matplotlib.pyplot.close()