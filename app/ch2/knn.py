# This code is supporting material for the book
# Building Machine Learning Systems with Python
# by Willi Richert and Luis Pedro Coelho
# published by PACKT Publishing
#
# It is made available under the MIT License

import numpy as np


def learn_model(k, features, labels):
    return k, features.copy(), labels.copy()


def plurality(xs):
    from collections import defaultdict
    counts = defaultdict(int)
    for x in xs:
        counts[x] += 1
    #print(counts)
    maxv = max(counts.values())
    #print(maxv)
    for k, v in counts.items():
        #print(k, v)
        if v == maxv:
            return k


def apply_model(features, model):
    k, train_feats, labels = model
    results = []
    for f in features:
        label_dist = []
        for t, ell in zip(train_feats, labels):
            label_dist.append((np.linalg.norm(f - t), ell))
        #print(label_dist)
        label_dist.sort(key=lambda d_ell: d_ell[0])
        #print(label_dist)
        label_dist = label_dist[:k]
        results.append(plurality([ell for _, ell in label_dist]))
    #print(results)
    return np.array(results)


def accuracy(features, labels, model):
    preds = apply_model(features, model)
    return np.mean(preds == labels)
