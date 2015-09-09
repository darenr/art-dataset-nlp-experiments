from nltk.corpus import wordnet as wn
from nltk.corpus.reader import NOUN
from gensim.models import Word2Vec
import os

model = Word2Vec.load_word2vec_format(os.environ['HOME'] + "/models/en_deps_300D_words.model")

def wv_synonyms(word):
  if word in model:
    return [x[0] for x in model.most_similar(word)[:5]]
  else:
    return []

def wn_synonyms(word):
  return [l.name().decode('utf-8') for l in wn.synset(word).lemmas()]

def wn_getword(word):
  return word.name().decode('utf-8')

for ss in ["gay.n.01", "portraiture.n.01", "folk_art.n.01", "gender_identity.n.01", "gender.n.02"]:

  print ss, ': wordnet:', ', '.join(wn_synonyms(ss))
  print ss, ': wordvec-first:', ', '.join(wv_synonyms(ss.split('.')[0]))
