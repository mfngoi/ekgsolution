import numpy as np # https://numpy.org/doc/stable/user/quickstart.html

# one dimension
a = np.arange(10)

# Properties
print(a.ndim)
print(a.shape)
print(a.dtype)

print(a)
print(a[2])
print(a[2:5])

# two dimension
def f(x, y):
    return 10 * x + y

b = np.fromfunction(f, (5, 4), dtype=int)

print(b)
print(b[2, 3])
print(b[0:5, 1])       # print(b[:, 1])
print(b[1:3, :])
