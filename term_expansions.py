from nltk.corpus import wordnet as wn
from nltk.corpus.reader import NOUN
from gensim.models import Word2Vec
import os

model = Word2Vec.load_word2vec_format(os.environ['HOME'] + "/models/en_deps_300D_words.model")
#model = Word2Vec.load_word2vec_format(os.environ['HOME'] + "/models/en_bow5_300d.model")
#model = Word2Vec.load_word2vec_format(os.environ['HOME'] + "/models/glove.42B.300d.txt", binary=False)
#model = Word2Vec.load_word2vec_format(os.environ['HOME'] + "/models/freebase-vectors-skipgram1000-en.bin.gz", binary=True)

def wv_synonyms(word):
  print 'expanding', word
  if word in model:
    # results are not sorted, so before we truncate let's sort them,
    sorted_sims = sorted(model.most_similar(word), key=lambda tup: tup[1])
    return [x[0] for x in sorted_sims if x[1] > 0.5]
  else:
    return []

for word in [ "cognitive dissonance", "political science", "urban development", "industrial development", "economic development"]:
  if len(word.split()) > 1:
    print wv_synonyms(word.replace(' ', '-'))
    print wv_synonyms(word.replace(' ', '_'))
  else:
    print wv_synonyms(word)
