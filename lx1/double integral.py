import scipy.integrate
from numpy import exp
import math 
f = lambda x, y : 16*x*y
g = lambda x : 0
h = lambda y : math.sqrt(1-4*y**2)
i = scipy.integrate.dblquad(f, 0, 0.5, g, h)
print (i)
