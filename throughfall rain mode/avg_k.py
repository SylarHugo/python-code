import numpy
import math
import scipy.integrate
import matplotlib.pyplot
# from mpl_toolkits.mplot3d import Axes3D
# import csv

R, H, G, pi = [30, 150, 70, math.pi]
f_k = 1
q = (1 - f_k * pi * pow(R, 2) / (3 * pow(G ,2)))
x = numpy.linspace(0, R, 200)
y = (1 - f_k + f_k * x / R)/q

fig = matplotlib.pyplot.figure(1)
figg = matplotlib.pyplot.subplot(111)
figgg = figg.plot(x, y)
x = numpy.linspace(R, G/2, 100)
y = 1 / q + x * 0
figgg = figg.plot(x, y)
matplotlib.pyplot.show()
