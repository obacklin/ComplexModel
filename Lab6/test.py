import numpy as np

a = np.zeros((3, 2))
b = np.array([1 ,2])

a[1] = b
c = a[0]

print(c)