# This code is supporting material for the book
# Building Machine Learning Systems with Python
# by Willi Richert and Luis Pedro Coelho
# published by PACKT Publishing
#
# It is made available under the MIT License

import numpy as np
import os

def join_base(path):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(base, path))


def load_dataset(dataset_name):
    '''
    data,labels = load_dataset(dataset_name)

    Load a given dataset

    Returns
    -------
    data : numpy ndarray
    labels : list of str
    '''
    data = []
    labels = []
    with open(join_base('../data/{0}.tsv'.format(dataset_name))) as ifile:
        for line in ifile:
            tokens = line.strip().split('\t')
            #print(tokens)
            data.append([float(tk) for tk in tokens[:-1]])
            labels.append(tokens[-1])
    data = np.array(data)
    labels = np.array(labels)
    return data, labels
