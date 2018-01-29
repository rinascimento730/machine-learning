# coding: utf-8
import numpy as np
print(np.version.full_version)

a = np.array([[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]])
a = np.array([[1,2,3],[4,5,6],[7,8,9],[10,11,12]])
a = np.array([0, 1, 2, 3, 4, 5])
print(a)
print(a.ndim)
print(a.shape)

b = a.reshape((3, 2))
print(b.ndim)
print(b.shape)

b[1][0]=77

print(a)
print(b)

c = a.reshape((3,2)).copy()
c[0][0] = -99

print(a)
print(c)

a = np.array([0, 1, 2, 3, 4, 5])
print(a*2)
print(a**2)

print(a[np.array([2,3,4])])

print(a < 4)

print(a[a>4])

a[a>4] = 4
print(a)

d = np.array([1, 2, np.NAN, 3, 4])
print(d)

print(np.isnan(d))
print(d[~np.isnan(d)])
print(np.mean(d[~np.isnan(d)]))

print(a.dtype)
print(b.dtype)
print(c.dtype)
print(d.dtype)

c = np.array([[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]])
d = np.array([0, 1, 2, 3, 4, 5])

print(c + d)
print(c.flatten())
print(d.reshape(3,2))
e = np.array([
		[1,2,3],
		[4,5,6],
		[7,8,9]
	])
print(np.diag(e))
print(np.diag(np.diag(e)))
print(e.transpose())
e[e >= 5] = 0
print(e)

f = np.array([
		[1,2,3],
		[4,5,6],
		[7,8,9]
	])

# 要素削除
g = np.delete(f, [0, 1], 0)
print(g)

h = np.delete(f, [0, 1], 1)
print(h)

# 行最大値抽出
print(np.max(f, axis = 0))
# 列最大値抽出
print(np.max(f, axis = 1))

i = np.arange(25).reshape(5,5)
print(i[:])
print(i[:3, :2])

j = np.array([
		[1,2,3,4],
		[5,6,7,8],
		[9,10,11,12],
		[13,14,15,16],
	])
print(np.delete(j, [0, 2], 0))

