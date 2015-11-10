from nltk.corpus import wordnet as wn
from nltk.corpus.reader import NOUN
from gensim.models import Word2Vec
import os

#model = Word2Vec.load_word2vec_format(os.environ['HOME'] + "/models/en_deps_300D_words.model")
#model = Word2Vec.load_word2vec_format(os.environ['HOME'] + "/models/en_bow5_300d.model")
model = Word2Vec.load_word2vec_format(os.environ['HOME'] + "/models/glove.42B.300d.txt", binary=False)

def wv_synonyms(word):
  w = '_'.join(word.split(' '))
  print 'expanding', word
  if w in model:
    # results are not sorted, so before we truncate let's sort them,
    sorted_sims = sorted(model.most_similar(w), key=lambda tup: tup[1])
    return [x[0] for x in sorted_sims if x[1] > 0.5]
  else:
    return []

for word in [ "globalization", "landscape", "abstraction", "appropriation"]:
  print word, wv_synonyms(word)
