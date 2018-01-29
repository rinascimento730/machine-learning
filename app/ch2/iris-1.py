# coding: utf-8
from matplotlib import pyplot as plt
from sklearn.datasets import load_iris
import numpy as np
import os

base = os.path.dirname(os.path.abspath(__file__))

# sklearnからload_iris関数を用いて、データをロードする
data = load_iris()
#print(data)
features = data['data']
feature_names = data['feature_names']
print(feature_names)
target = data['target']
print(target)


pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
for i, (p0, p1) in enumerate(pairs):
    plt.subplot(2, 3, i + 1)
    for t, marker, c in zip(range(3), ">ox", "rgb"):
        plt.scatter(features[target == t, p0], features[
                    target == t, p1], marker=marker, c=c)
    plt.xlabel(feature_names[p0])
    plt.ylabel(feature_names[p1])
    plt.xticks([])
    plt.yticks([])
filename = os.path.normpath(os.path.join(base, '../../output/iris-data-matrix.png'))
plt.savefig(filename)

target_names = data['target_names']
print(target_names)
labels = target_names[target]
print(labels)

for t,marker,c in zip(range(3),">ox","rgb"):
	# クラスごとに色の異なるマーカでプロットする
	plt.scatter(features[target == t,0],
				features[target == t,1],
				marker=marker,
				c=c)
filename = os.path.normpath(os.path.join(base, '../../output/iris-data-matrix_old.png'))
plt.savefig(filename)