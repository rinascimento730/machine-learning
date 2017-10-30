# coding: utf-8
import scipy as sp
import numpy as np
import os
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

def error(f, x, y):
	return sp.sum((f(x)-y)**2)

#print(sp.version.full_version)
#print(sp.dot is np.dot)

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

fp1, residuals, rank, sv, rcond = sp.polyfit(x, y, 1, full=True)
print("Model parameters: %s" % fp1)
print(residuals)

f1 = sp.poly1d(fp1)
print(error(f1, x, y))

fp2, residuals2, rank2, sv2, rcond2 = sp.polyfit(x, y, 2, full=True)
print("Model parameters: %s" % fp2)
print(residuals2)

f2 = sp.poly1d(fp2)
print(error(f2, x, y))

fp3, residuals3, rank3, sv3, rcond3 = sp.polyfit(x, y, 3, full=True)
print("Model parameters: %s" % fp3)
print(residuals3)

f3 = sp.poly1d(fp3)
print(error(f3, x, y))

fp4, residuals4, rank4, sv4, rcond4 = sp.polyfit(x, y, 4, full=True)
print("Model parameters: %s" % fp4)
print(residuals4)

f4 = sp.poly1d(fp4)
print(error(f4, x, y))

plt.scatter(x,y)
plt.plot(x, f4(x), color="orange", linewidth=2)
plt.plot(x, f3(x), color="red", linewidth=2)
plt.plot(x, f2(x), color="yellow", linewidth=2)
plt.plot(x, f1(x), color="purple", linewidth=2)
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


inflection = int(3.5*7*24)
print(inflection)
xa = x[:inflection] # 変化点前のデータポイント
ya = y[:inflection]
xb = x[inflection:] # 変化点後のデータポイント
yb = y[inflection:]

frac = 0.3 # テストに用いるデータの割合
split_idx = int(frac * len(xb))
# 全データの30%をランダムに選び出す
shuffled = sp.random.permutation(list(range(len(xb))))
test = sorted(shuffled[:split_idx]) # テスト用のデータインデックス配列
train = sorted(shuffled[split_idx:]) # 訓練用のデータインデックス配列
#それぞれ訓練データを用いて訓練を行う
fbt1 = sp.poly1d(sp.polyfit(xb[train], yb[train], 1))
fbt2 = sp.poly1d(sp.polyfit(xb[train], yb[train], 2))
fbt3 = sp.poly1d(sp.polyfit(xb[train], yb[train], 3))
fbt10 = sp.poly1d(sp.polyfit(xb[train], yb[train], 10))
#それぞれテストデータを用いて評価を行う
for f in [fbt1, fbt2, fbt3, fbt10]:
	print("Error d=%i: %f" % (f.order, error(f, xb[test], yb[test])))

print(fbt2)

reached_max = fsolve(fbt2-100000, 800)/(7*24)
print(reached_max)
print("100,000 hits/hour expected at week %f" % reached_max[0])

