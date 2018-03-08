# coding: utf-8
import os
import scipy as sp
import sklearn.datasets
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk.stem
from sklearn.cluster import KMeans
from sklearn import metrics

english_stemmer = nltk.stem.SnowballStemmer('english')
new_post = \
    """Disk drive problems. Hi, I have a problem with my hard disk.
After 1 year it is working only sporadically now.
I tried to format it, but now it doesn't boot any more.
Any ideas? Thanks.
"""

def join_base(path):
    base = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(base, path))

class StemmedTfidfVectorizer(TfidfVectorizer):
    def build_analyzer(self):
        analyzer = super(TfidfVectorizer, self).build_analyzer()
        return lambda doc: (english_stemmer.stem(w) for w in analyzer(doc))

def get_data(data_type = 'train'):
    MLCOMP_DIR = join_base('./data/')
    groups = ['comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware',
              'comp.sys.mac.hardware', 'comp.windows.x', 'sci.space']
    data = sklearn.datasets.load_mlcomp("20news-18828", data_type,
                                       mlcomp_root=MLCOMP_DIR,
                                       categories=groups)
    return data

def print_km_metric(km, labels, vectorized):
  print("", end="\n")
  print("Homogeneity: %0.3f" % metrics.homogeneity_score(labels, km.labels_))
  print("Completeness: %0.3f" % metrics.completeness_score(labels, km.labels_))
  print("V-measure: %0.3f" % metrics.v_measure_score(labels, km.labels_))
  print("Adjusted Rand Index: %0.3f" %
        metrics.adjusted_rand_score(labels, km.labels_))
  print("Adjusted Mutual Information: %0.3f" %
        metrics.adjusted_mutual_info_score(labels, km.labels_))
  print(("Silhouette Coefficient: %0.3f" %
         metrics.silhouette_score(vectorized, labels, sample_size=1000)), end="\n\n")


def learn_km_model(data, num_clusters = 8):
    vectorizer = StemmedTfidfVectorizer(min_df=10, max_df=0.5, stop_words='english', decode_error='ignore')
    #print(vectorizer)
    #print(train_data.data)
    vectorized = vectorizer.fit_transform(data.data)
    num_samples, num_features = vectorized.shape
    print("#samples: %d, #features: %d" % (num_samples, num_features))

    #km = KMeans(n_clusters=num_clusters, init='random', n_init=1, verbose=1)
    km = KMeans(n_clusters=num_clusters, init='k-means++', n_init=1, verbose=1)
    km.fit(vectorized)

    #print(km.labels_)
    #print(km.labels_.shape)
    #print(len(km.cluster_centers_))
    return km, vectorizer, vectorized

def main():
    train_data = get_data("train")
    #print(train_data.filenames)
    #print(len(train_data.filenames))
    #print(train_data.target_names)

    km, vectorizer, vectorized = learn_km_model(train_data, 50)
    print_km_metric(km, train_data.target, vectorized)

    new_post_vec = vectorizer.transform([new_post])
    new_post_label = km.predict(new_post_vec)[0]
    print(new_post_label)
    similar_indices = (km.labels_==new_post_label).nonzero()[0]
    print(similar_indices)
    #print(train_data.data[similar_indices[0]])

    # 3.4
    similar = []
    for i in similar_indices:
      dist = sp.linalg.norm((new_post_vec - vectorized[i]).toarray())
      similar.append((dist, train_data.data[i]))
    similar = sorted(similar)
    print(len(similar))
    #print(similar)
    show_at_1 = similar[0]
    print(show_at_1)

    # 3.4.1 Noise
    post_group = zip(train_data.data, train_data.target)
    z = [(len(post[0]), post[0], train_data.target_names[post[1]]) for post in post_group]
    print(sorted(z)[5:7])

    analyzer = vectorizer.build_analyzer()
    print(list(analyzer(z[5][1])))
    print(list(analyzer(z[6][1])), end="\n\n")

    a = list(set(analyzer(z[5][1])).intersection(vectorizer.get_feature_names()))
    a += list(set(analyzer(z[6][1])).intersection(vectorizer.get_feature_names()))

    for term in a:
      print('IDF(%s)=%.2f'%(term, vectorizer._tfidf.idf_[vectorizer.vocabulary_[term]]))

if __name__ == "__main__":
    main()