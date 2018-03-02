# coding: utf-8
from matplotlib import pyplot as plt
from sklearn.datasets import load_iris
import numpy as np
import statistics as st
import treshold
import os
from sklearn.model_selection import KFold

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

def is_type(labels, iris_type):
    return (labels == iris_type)

def get_setosa_threshold(features, labels):
    #「花弁の長さ」は配列の3番目(インデックス操作では2)に格納されている
    plength = features[:, 2]
    is_setosa = is_type(labels, 'setosa') # setosaかどうかのブーリアン配列を生成

    # 次が重要なステップ
    max_setosa =plength[is_setosa].max()
    min_non_setosa = plength[~is_setosa].min()
    print('Maximum of setosa: {0}.'.format(max_setosa))
    print('Minimum of others: {0}.'.format(min_non_setosa))

    setosa_threshold = st.mean([max_setosa, min_non_setosa])

    return setosa_threshold

def learn_model(features, labels):
    best_acc = 0
    best_acc_alt = 0
    #print(features)
    #print(features.shape[1])
    #print(len(labels))
    #print(labels)
    for fi in range(features.shape[1]):
        thresh = features[:, fi].copy()
        thresh.sort()
        for t in thresh:
            pred = (features[:, fi] > t)
            #print(pred)
            #acc_1 = (labels[pred] == 'virginica').sum()
            #acc_2 = (labels[~pred] == 'versicolor').sum()
            #acc = (acc_1 + acc_2) / len(labels)
            acc = (pred == (labels == 'virginica')).mean()
            #print(acc, acc_1, acc_2)
            #print(labels[pred])
            if acc > best_acc:
                best_acc = acc
                best_fi = fi
                best_t = t

    print('best_acc:', best_acc)
    return best_t, best_fi

def accuracy(pred, label):
    return (pred == label)


def apply_model(features, labels, model):
    t, fi = model
    #print("apply_model ")
    #print(fi, t)
    correct = []
    setosa_threshold = get_setosa_threshold(features, labels)
    print("setosa treshold: ",setosa_threshold)

    for feature, label in zip(features, labels):
        pred = ''
        if feature[2] < setosa_threshold:
            pred = 'setosa'
        else:
            if feature[fi] > t:
                pred = 'virginica'
            else:
                pred = 'versicolor'
        #print(label, pred)

        correct.append(accuracy(pred, label))
    # print(correct)
    #print(len(correct))

    return np.array(correct).mean()

def prepare_virginica_treshold(features, labels):
    is_setosa = is_type(labels, 'setosa')
    not_setosa_features = features[~is_setosa]
    not_setosa_labels = labels[~is_setosa]
    best_t, best_fi = learn_model(not_setosa_features, not_setosa_labels)
    #print("best_t, best_fi: ", best_t, best_fi)

    return best_t, best_fi

def main():
    features, feature_names, target, target_names, labels = get_iris_data()
    plot_data(features, feature_names, target)

    kf = KFold(n_splits = 5, shuffle = True)
    kf_acc = []
    for train_index, test_index in kf.split(features):
        #print(train_index, test_index)
        #print(labels[test_index])
        model = prepare_virginica_treshold(features[train_index], labels[train_index])
        #acc_train = apply_model(features[train_index], labels[train_index])
        acc_test = apply_model(features[test_index], labels[test_index], model)
        print(acc_test, end='\n\n')
        kf_acc.append(acc_test)
    kf_acc_score = np.array(kf_acc).mean()
    print("kf_acc_score")
    print(kf_acc_score, end='\n\n')

    print("all data")
    model = prepare_virginica_treshold(features, labels)
    acc = apply_model(features, labels, model)
    print(acc, end='\n\n')

if __name__ == "__main__":
    print("exec!")
    main()

#print('モジュール名：{}'.format(__name__))