import json
import sys
import itertools
import codecs
from textblob import TextBlob, Word
from textblob.wordnet import Synset

def wn_hypernyms(w):
  return [s._name for s in Synset(w).hypernyms()] if '.' in w else []

if len(sys.argv) < 2:
  print 'usage: <synset, eg. "utopia.n.04">'
  sys.exit(-1)
else:
  for x in range(1,len(sys.argv)):
    print sys.argv[x], 'hypernyms:', wn_hypernyms(sys.argv[x])
