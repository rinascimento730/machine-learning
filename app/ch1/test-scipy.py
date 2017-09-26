# coding: utf-8
import scipy as sp
import numpy as np
import os
import matplotlib.pyplot as plt

print(sp.version.full_version)
print(sp.dot is np.dot)

base = os.path.dirname(os.path.abspath(__file__))
file = os.path.normpath(os.path.join(base, '../../BuildingMachineLearningSystemsWithPython/ch01/data/web_traffic.tsv'))
data = sp.genfromtxt(file, delimiter="\t")
print(data[:10])
print(data.shape)

x = data[:,0]
y = data[:,1]
x = x[~sp.isnan(y)]
y = y[~sp.isnan(y)]
#print(x)
#print(y)

print(sp.sum(sp.isnan(y)))

plt.scatter(x,y)
plt.title("Web traffic over the last month")
plt.xlabel("Time")
plt.ylabel("Hits/hour")
plt.xticks([w*7*24 for w in range(10)],
['week %i'%w for w in range(10)])
plt.autoscale(tight=True)
plt.grid()
filename = os.path.normpath(os.path.join(base, '../../output/web-trafic-over-the-las-month.png'))
plt.savefig(filename)
#plt.show()
