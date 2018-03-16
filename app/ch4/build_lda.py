# This code is supporting material for the book
# Building Machine Learning Systems with Python
# by Willi Richert and Luis Pedro Coelho
# published by PACKT Publishing
#
# It is made available under the MIT License

import nltk.corpus
import milk
import numpy as np
import string
from gensim import corpora, models, similarities
import sklearn.datasets
import nltk.stem
from collections import defaultdict
import os

english_stemmer = nltk.stem.SnowballStemmer('english')
stopwords = set(nltk.corpus.stopwords.words('english'))
stopwords.update(['from:', 'subject:', 'writes:', 'writes'])

def join_base(path):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(base, path))

class DirectText(corpora.textcorpus.TextCorpus):

    def get_texts(self):
        return self.input

    def __len__(self):
        return len(self.input)

def get_dataset():
    MLCOMP_DIR = join_base('../ch3/data/')
    print(MLCOMP_DIR)
    dataset = sklearn.datasets.load_mlcomp("20news-18828", "raw", mlcomp_root=MLCOMP_DIR)
    return dataset

def main():
    dataset = get_dataset()
    otexts = dataset.data
    texts = dataset.data

    texts = [t.decode('utf-8', 'ignore') for t in texts]
    texts = [t.split() for t in texts]
    texts = [map(lambda w: w.lower(), t) for t in texts]
    texts = [filter(lambda s: not len(set("+-.?!()>@012345689") & set(s)), t)
             for t in texts]
    texts = [filter(lambda s: (len(s) > 3) and (s not in stopwords), t)
             for t in texts]
    texts = [map(english_stemmer.stem, t) for t in texts]
    usage = defaultdict(int)
    for t in texts:
        for w in set(t):
            usage[w] += 1
    limit = len(texts) / 10
    too_common = [w for w in usage if usage[w] > limit]
    too_common = set(too_common)
    texts = [filter(lambda s: s not in too_common, t) for t in texts]
    #print(texts)
    corpus = DirectText(texts)
    dictionary = corpus.dictionary
    try:
        dictionary['computer']
    except:
        print("except")
        pass
    print(len(corpus))
    #print(len(corpus.id2token))
    print(dir(dictionary))
    print(dictionary.id2token)
    exit()
    model = models.ldamodel.LdaModel(
        corpus, num_topics=100, id2word=dictionary.id2token)

    thetas = np.zeros((len(texts), 100))
    for i, c in enumerate(corpus):
        for ti, v in model[c]:
            thetas[i, ti] += v
    distances = milk.unsupervised.pdist(thetas)
    print(distances)
    exit()
    large = distances.max() + 1
    for i in xrange(len(distances)):
        distances[i, i] = large

    print(otexts[1])
    print()
    print()
    print()
    print(otexts[distances[1].argmin()])


if __name__ == "__main__":
    main()