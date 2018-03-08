# coding: utf-8
from matplotlib import pyplot as plt
import numpy as np
import statistics as st
import os
import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy as sp
import nltk.stem

english_stemmer = nltk.stem.SnowballStemmer('english')

class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

def join_base(path):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(base, path))

def dist_raw(v1, v2):
    delta = v1-v2
    #print("v1")
    #print(v1)
    #print("v2")
    #print(v2)
    #print("delta")
    #print(delta)
    return sp.linalg.norm(delta.toarray())

def get_posts():
    DIR = join_base('./data/text')
    posts = [open(os.path.join(DIR, f)).read() for f in os.listdir(DIR)]
    print(posts)

    return posts

def dist_norm(v1, v2):
    v1_normalized = v1/sp.linalg.norm(v1.toarray())
    v2_normalized = v2/sp.linalg.norm(v2.toarray())
    delta = v1_normalized - v2_normalized
    return sp.linalg.norm(delta.toarray())

def tfidf(term, doc, docset):
    # sklearnのTfidfVectorizerを使えばいい
    tf = float(doc.count(term))/sum(doc.count(w) for w in set(doc))
    idf = math.log(float(len(docset))/(len([doc for doc in docset if term in doc])))
    return tf * idf

def apply_model(vectorizer, posts, new_post):
    X_train = vectorizer.fit_transform(posts)
    num_samples, num_features = X_train.shape
    print("#samples: %d, #features: %d" % (num_samples, num_features))
    print(vectorizer.get_feature_names())
    #print(X_train.toarray().transpose())
    #print(X_train.toarray())

    new_post_vec = vectorizer.transform([new_post])
    #print(new_post_vec)
    #print(new_post_vec.toarray())

    best_doc = None
    best_dist = sys.maxsize
    best_i = None
    best_dist_norm = sys.maxsize
    best_i_norm = None

    for i in range(0, num_samples):
        post = posts[i]
        if post == new_post:
            continue
        post_vec = X_train.getrow(i)
        #print(post_vec)
        d = dist_raw(post_vec, new_post_vec)
        d_norm = dist_norm(post_vec, new_post_vec)
        print("=== Post %i with dist=%.2f: %s"%(i, d, post))
        print("=== Post %i with dist_norm=%.2f: %s"%(i, d_norm, post))
        if d < best_dist:
            best_dist = d
            best_i = i
        if d_norm < best_dist_norm:
            best_dist_norm = d_norm
            best_i_norm = i
    print("Best post is %i with dist=%.2f"%(best_i, best_dist))
    print("Best post is %i with dist_norm=%.2f"%(best_i_norm, best_dist_norm), end="\n\n")

    #print(X_train.getrow(3).toarray())
    #print(X_train.getrow(4).toarray())


def main():
    vectorizer = CountVectorizer(min_df=1)
    #print(vectorizer)

    content = ["How to format my hard disk", " Hard disk format problems "]
    X = vectorizer.fit_transform(content)
    test = vectorizer.get_feature_names()
    #print(test)
    #print(X.toarray().transpose())

    posts = get_posts()
    new_post = "imaging databases"

    # basic
    print("basic")
    apply_model(vectorizer, posts, new_post)

    # stop_words
    print("stop_words")
    vectorizer2 = CountVectorizer(min_df=1, stop_words='english')
    #print(sorted(vectorizer2.get_stop_words())[0:20])
    apply_model(vectorizer2, posts, new_post)

    # stop_words + stemming
    print("stop_words + stemming")
    vectorizer3 = StemmedCountVectorizer(min_df=1, stop_words='english')
    apply_model(vectorizer3, posts, new_post)

    # stop_words + stemming + TF-IDF
    print("stop_words + stemming + TF-IDF")
    vectorizer4 = StemmedTfidfVectorizer(min_df=1, stop_words='english')
    apply_model(vectorizer4, posts, new_post)


if __name__ == "__main__":
    main()