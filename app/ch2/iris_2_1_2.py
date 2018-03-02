# coding: utf-8
from matplotlib import pyplot as plt
import numpy as np
import iris_2_1_1 as iris_base

def get_iris_data():
    data = iris_base.load_iris_data()
    features = data['data']
    feature_names = data['feature_names']
    species = data['target_names'][data['target']]

    #print(features[0])
    #print(data['target'])
    #print(data['target_names'])
    #print(feature_names)

    return features, feature_names, species

def extract_setosa_feature(features, species):
    #「花弁の長さ」は配列の3番目(インデックス操作では2)に格納されている
    plength = features[:, 2]
    is_setosa = (species == 'setosa') # setosaかどうかのブーリアン配列を生成

    # 次が重要なステップ
    max_setosa =plength[is_setosa].max()
    min_non_setosa = plength[~is_setosa].min()
    setosa_threshold = (min_non_setosa - max_setosa / 2) if max_setosa < min_non_setosa else 0
    print('Maximum of setosa: {0}.'.format(max_setosa))
    print('Minimum of others: {0}.'.format(min_non_setosa))

    return (max_setosa, min_non_setosa, setosa_threshold)

def apply_model(feature, setosa_threshold):
    if feature[2] < setosa_threshold:
        print('Iris Setosa')
    else:
        print('Iris Virginica or Iris Versicolor')

def main():
    features, feature_names, species = get_iris_data()
    #print(species)

    max_setosa, min_non_setosa, setosa_threshold = extract_setosa_feature(features, species)
    #print(max_setosa, min_non_setosa)

    if setosa_threshold > 0:
        for i, feature in enumerate(features):
            #print(i, ":")
            apply_model(feature, setosa_threshold)
    else:
        print("Can't classify")

if __name__ == "__main__":
    main()