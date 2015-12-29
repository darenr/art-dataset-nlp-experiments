from nltk.corpus import wordnet as wn
from nltk.corpus.reader import NOUN
import os

# sister terms are synsets that share a common hypernym

def wn_synonyms(ss):
  return [l.name().decode('utf-8') for l in ss.lemmas()]

def wn_getword(ss):
  return ss if isinstance(ss, basestring) else ss.name().decode('utf-8').split('.')[0]

def wn_make_synset(word):
  if '.' in word:
    return wn.synset(word)
  else:
    ss = wn.synsets(word, NOUN)
    if ss:
      return ss[0]
    else:
      return None

for word in [ "transience" ]:

  synonyms = []

  ss = wn_make_synset(word)
  if ss:
    synonyms += wn_synonyms(ss)

  synonyms = list(set(synonyms))

  print word, synonyms
