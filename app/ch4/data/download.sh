#!/bin/sh
cd /vagrant/app/ch4/data/
wget http://www.cs.columbia.edu/~blei/lda-c/ap.tgz
tar xzf ap.tgz
wget http://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2
python3.6 -m gensim.scripts.make_wiki enwiki-latest-pages-articles.xml.bz2 ./wiki_en_output
