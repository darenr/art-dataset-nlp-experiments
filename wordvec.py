from gensim.models import Word2Vec
model = Word2Vec.load("/home/drace/word2vec_models/en_1000_nostem/en.model")
model.similarity('woman', 'man')
