# #epsabs=1.49e-06, epsrel=1.49e-06#精度
# import numpy
# import scipy.integrate
# import matplotlib.pyplot
# from mpl_toolkits.mplot3d import Axes3D
# import csv
# import math
# #initial_value：冠幅，间距，冠高，面积，半径，分段个数，容差范围值，R, B, H, square_dm, radius, step_point, accept_p
# accept_p = numpy.zeros(2)
# #基本参数设置
# H, R, B, S, pi, step_point, canot_accept = [50, 30, 10, 60 ,math.pi, 36, 5]
# radius = numpy.sqrt(S / pi)#圆的半径
# V_circle = S * H
# R2 = pow(R, 2)
# r2 = pow(radius, 2)
# step_range = range(0, step_point, 1)#生成分割序列
# mode_limit = R + B / 2
# d_limit = mode_limit / (step_point - 1)#分割段长度
# rain_out = pow(mode_limit, 2) * H
#
# canopy_interception = pi * R2 * H / 12
# throughfall = rain_out - canopy_interception#林分穿透雨
# percentage = throughfall / rain_out#林分穿透雨占比
# accept_p = [percentage * (100 - canot_accept), percentage * (100 + canot_accept)]#水槽测的穿透雨的容差范围值
#
# #四个树冠的圆心
# def canopy_center():#四个树冠的圆心
#     canopy_center_point = numpy.zeros((4, 2))
#     canopy_center_point[0][0] = 0
#     canopy_center_point[0][1] = 0
#     canopy_center_point[1][0] = 2 * R + B
#     canopy_center_point[1][1] = 0
#     canopy_center_point[2][0] = 2 * R + B
#     canopy_center_point[2][1] = 2 * R + B
#     canopy_center_point[3][0] = 0
#     canopy_center_point[3][1] = 2 * R + B
#     return canopy_center_point
# canopy_dot = canopy_center()#四个树冠的圆心
# #第i个树冠体积函数
# def f_canopy(i):#i=tree_num
#     return lambda x, y: H - numpy.sqrt((x - canopy_dot[i][0]) ** 2 + (y - canopy_dot[i][1]) ** 2) * H / R
# #第i个树冠的上半圆函数
# def func_up_canopy(i):#i=tree_num
#     return lambda x: canopy_dot[i][1] + numpy.sqrt(R2 - (x - canopy_dot[i][0]) ** 2)#上半圆函数
# #第i个树冠的下半圆函数
# def func_down_canopy(i):#i=tree_num
#     return lambda x: canopy_dot[i][1] - numpy.sqrt(R2 - (x - canopy_dot[i][0]) ** 2)#下半圆函数
# #水槽上半圆函数
# def f_up_circle(circle_dot):
#     return lambda x: circle_dot[1] + numpy.sqrt(r2 - (x - circle_dot[0]) ** 2)
# #水槽下半圆函数
# def f_down_circle(circle_dot):
#     return lambda x: circle_dot[1] - numpy.sqrt(r2 - (x - circle_dot[0]) ** 2)
# # 返回交点a的X,b的X
# def f_canopy_intersection_circle(point_a, point_b, d):
#     R_ortho = (R2 - r2 + pow(d, 2)) / (2 * d)
#     h_ortho = numpy.sqrt(R2 - pow(R_ortho, 2))
#     x_o = point_a[0] + R_ortho * (point_b[0] - point_a[0]) / d
#     y_o = point_a[1] + R_ortho * (point_b[1] - point_a[1]) / d
#     x1 = x_o - h_ortho * (point_b[1] - point_a[1]) / d
#     x2 = x_o + h_ortho * (point_b[1] - point_a[1]) / d
#     y1 = x_o - h_ortho * (point_b[0] - point_a[0]) / d
#     y2 = x_o + h_ortho * (point_b[0] - point_a[0]) / d
#     return x1, x2
# #两点间距离
# def f_distance(point_a, point_b):
#     distance_value = numpy.sqrt(pow((point_a[0] - point_b[0]), 2) + pow((point_a[1] - point_b[1]), 2))
#     return distance_value
# #生成水槽中心点数组，第一维：某点的穿透雨量、X轴坐标、Y轴坐标，第二维X轴定值的Y轴点集合，第三维X轴的集合
# ucs = numpy.zeros((step_point, step_point, 3))#中心点数组：截留量、X、Y坐标
# #对水槽中心点数组赋值X、Y坐标
# for i in step_range:#对水槽中心点数组赋值X、Y坐标
#     for j in step_range:
#         ucs[i][j][1] = d_limit * i
#         ucs[i][j][2] = d_limit * j
# #赋值：xa,xb,2个ab交点，2个cd焦点和圆左右边界 的X轴坐标集合，6个数，分段积分：5段
# def intersection_point_sequence(tree, circle_dot):
#     c_i_s_get = numpy.zeros(6)#第7个和第8个为交点的Y值
#     c_i_s_get[0] = circle_dot[0] - radius#圆左界x
#     c_i_s_get[1] = circle_dot[0] + radius#圆右界x
#     c_i_s_get[2] = c_i_s_get[0]#圆左交点
#     c_i_s_get[3] = c_i_s_get[0]#圆右交点
#     c_i_s_get[4] = canopy_dot[tree][0] - R#树冠左边界
#     c_i_s_get[5] = canopy_dot[tree][0] + R#树冠右边界
#     distance = f_distance(canopy_dot[tree], circle_dot)
#     if R - radius < distance < R + radius:
#         c_i_s_get[2], c_i_s_get[3] = f_canopy_intersection_circle(canopy_dot[tree], circle_dot, distance)
#     return c_i_s_get, distance#排升序
# #对各长方形4个点赋值，并求与4个树冠相交部分的截留量
# for one_dimensional in ucs:#第三维
#     for two_dimensional in one_dimensional:#第二维
#         circle_dot = numpy.zeros(2)  # 生成圆心的数组
#         canopy_interception = numpy.zeros(4)  # 4个树冠的截留量
#         circle_dot[0] = two_dimensional[1]#xa
#         circle_dot[1] = two_dimensional[2]#ya
#         #xa,xb,2个ab交点，2个cd焦点，R的集合，分段积分-6段
#         for tree in range(0, 4, 1):
#             #交点赋值、两圆圆心距离
#             c_i_s, distance_dot = intersection_point_sequence(tree, circle_dot)
#             left_limit = max(c_i_s[0], c_i_s[4])
#             right_limit = min(c_i_s[1], c_i_s[5])
#             if distance_dot >= R + radius:
#                 canopy_interception[tree] = 0
#             elif distance_dot <= R - radius:
#                 func_g = f_down_circle(circle_dot)
#                 func_h = f_up_circle(circle_dot)
#                 a = c_i_s[0]
#                 b = c_i_s[1]
#                 canopy_interception[tree] = scipy.integrate.dblquad(f_canopy(tree), a, b, func_g, func_h,
#                                                         epsabs=1.49e-06, epsrel=1.49e-06)[0]
#             elif R - radius < distance_dot < R + radius:
#                 # 第i个树冠的分段截留量
#                 rain_i = numpy.zeros(5)
#                 for i in range(0, 5, 1):
#                     c_i_s = sorted(c_i_s)
#                     if left_limit <= c_i_s[i] < c_i_s[i + 1] <= right_limit:
#                         a = c_i_s[i]
#                         b = c_i_s[i + 1]
#                         midpoint_x = (a + b) / 2
#                         cir_mid_up_y = f_up_circle(circle_dot)(midpoint_x)
#                         cir_mid_down_y = f_down_circle(circle_dot)(midpoint_x)
#                         canopy_mid_up_y = func_up_canopy(tree)(midpoint_x)
#                         canopy_mid_down_y = func_down_canopy(tree)(midpoint_x)
#                         if cir_mid_up_y <= canopy_mid_down_y or cir_mid_down_y >= canopy_mid_up_y:
#                             continue
#                         if cir_mid_down_y > canopy_mid_down_y:
#                             func_g = f_down_circle(circle_dot)
#                         else:
#                             func_g = func_down_canopy(tree)
#                         if cir_mid_up_y < canopy_mid_up_y:
#                             func_h = f_up_circle(circle_dot)
#                         else:
#                             func_h = func_up_canopy(tree)
#                         rain_i[i] = scipy.integrate.dblquad(f_canopy(tree), a, b, func_g, func_h,
#                                                         epsabs=1.49e-06, epsrel=1.49e-06)[0]
#                 canopy_interception[tree] = numpy.sum(numpy.abs(rain_i))
#         two_dimensional[0] = 100 * (V_circle - numpy.sum(canopy_interception))/V_circle
# # # #生成X,Y的集合
# # # ucs_x = numpy.linspace(0, mode_limit, step_point)
# # # ucs_y = numpy.linspace(0, mode_limit, step_point)
# # # UX, UY = numpy.meshgrid(ucs_x, ucs_y)#meshgrid函数用两个坐标轴上的点在平面上画格
# # #生成穿透雨量的二维矩阵，并赋值
# ucs_rain = numpy.zeros((step_point, step_point))
# # #ucs_rain_T = numpy.zeros(step_point, step_point)
# circle_p_num = 0
# for i in step_range:#第一维
#     for j in step_range:#第二维
#         ucs_rain[j][i] = ucs[i][j][0]
#         #ucs_rain_T[i][j] = ucs[i][j][0]
#         if accept_p[0] < ucs[i][j][0] < accept_p[1]:
#             circle_p_num = circle_p_num + 1
# ucs_x = numpy.linspace(0, mode_limit, step_point)
# ucs_y = numpy.linspace(0, mode_limit, step_point)
# UX, UY = numpy.meshgrid(ucs_x, ucs_y)#meshgrid函数用两个坐标轴上的点在平面上画格
# fig = matplotlib.pyplot.figure()
# ax = fig.add_subplot(111, projection='3d')
# #ax.plot_trisurf(UX, UY, ucs_rain, linewidth=0.2, antialiased=True)
# ax.plot_wireframe(UX, UY, ucs_rain, rstride=10, cstride=10)
# matplotlib.pyplot.show()
# a = 1