# coding: utf-8
from matplotlib import pyplot as plt
from sklearn.datasets import load_iris
import numpy as np
import os

def join_base(path):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(base, path))

def load_iris_data():
    # sklearnからload_iris関数を用いて、データをロードする
    data = load_iris()
    return data

def get_iris_data():
    data = load_iris_data()
    features = data['data']
    feature_names = data['feature_names']
    target = data['target']
    target_names = data['target_names']
    labels = target_names[target]

    return features, feature_names, target, target_names, labels

def plot_data(features, feature_names, target):
    pairs = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
    for i, (p0, p1) in enumerate(pairs):
        #print(i, (p0, p1))
        plt.subplot(2, 3, i + 1)

        for t, marker, c in zip(range(3), ">ox", "rgb"):
            #if i == 0:
                #print(t, marker, c)
            plt.scatter(features[target == t, p0], features[
                        target == t, p1], marker=marker, c=c, s=10)
        plt.xlabel(feature_names[p0])
        plt.ylabel(feature_names[p1])
        plt.xticks([])
        plt.yticks([])
    plt.savefig(join_base('output/iris-data-matrix.png'))

def main():
    features, feature_names, target, target_names, labels = get_iris_data()
    plot_data(features, feature_names, target)

if __name__ == "__main__":
    print("exec!")
    main()

#print('モジュール名：{}'.format(__name__))