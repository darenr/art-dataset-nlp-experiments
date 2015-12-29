import sys
import codecs
from textblob import Blobber
from textblob.wordnet import Synset
from textblob.en.np_extractors import ConllExtractor
from collections import Counter
import re
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import NOUN
import os
import string
import itertools
from nltk.corpus import stopwords

stoplist = stopwords.words('english')
stoplist.extend(stopwords.words('french'))

stoplist.extend(["cette", "made", "works", "image", "images", "les", "comme"])
stoplist.extend(["photograph", "photographer", "film", "untitled", "series", "artist"])
stoplist.extend(["photographs", "other", "like", "also", "said", "work", "one", "two", "three"])
stoplist.extend(list(string.ascii_lowercase))


def wn_synonyms(ss):
  return [l.name().decode('utf-8') for l in ss.lemmas()]

def wn_expand(ss):
  x= [wn_getword(ss)]
  b = tb(ss.definition())
  x.extend([t[0] for t in b.tags if t[1] in ['JJ', 'NN', 'NNS']])
  return x

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

def contains_number(word):
  return re.search(r'[0-9]', word) 

def bad(word):
  return contains_number(word) or word.lower() in stoplist or len(word) < 3

tb = Blobber(np_extractor=ConllExtractor())

if __name__ == "__main__":
  for arg in sys.argv[1:]:
    with codecs.open(arg, 'r', encoding='utf-8') as f:
      text = f.read()
      b = tb(text)
      step1 = [t[0] for t in b.tags if t[1] in ['JJ', 'NN', 'NNS'] and not bad(t[0])]

      #step2 = [wn_make_synset(word) for word in step1 if wn_make_synset(word)]
      #step3 = list(itertools.chain.from_iterable([wn_expand(ss) for ss in step2]))

      print "\n"
      print '=' *60
      print arg
      print '=' *60
      print ' *', Counter(step1)

