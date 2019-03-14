import numpy as np
import timeit
import ipython
xx = np.zeros(100000000)
t=timeit.tiemit(xx[:] = 1 )

s='''xx <- rep(0, 100000000)
system.time(xx[] <- 1)
user  system elapsed 
  1.326   0.103   1.433'''
