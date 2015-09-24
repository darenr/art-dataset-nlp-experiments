import json
import sys
import itertools
import codecs
from textblob import TextBlob, Word
from textblob.wordnet import Synset

def is_synset(w):
  return 'n.0' in w

def wn_hypernym(w):
 ss = Synset(w)
 return [s._name for s in ss.hypernyms()]

def load_data(filename):
  with codecs.open(filename, 'rb', 'utf-8') as f:
    kadist = json.loads(f.read())
    for m in kadist:
      m['major_tag_hypernyms'] = []
      m['minor_tag_hypernyms'] = []
      if len(m['major_tags']):
        m['major_tag_hypernyms'].extend(list(itertools.chain.from_iterable([wn_hypernym(w) for w in m['major_tags'] if is_synset(w)])))
        print m['major_tag_hypernyms']
      if len(m['minor_tags']):
        m['minor_tag_hypernyms'].extend(list(itertools.chain.from_iterable([wn_hypernym(w) for w in m['minor_tags'] if is_synset(w)])))
        print m['minor_tag_hypernyms']
    
  with codecs.open('_kadist.json', 'wb', 'utf-8') as out:
    out.write(json.dumps(kadist, indent=2, ensure_ascii=False))
  

if len(sys.argv) != 2:
  print 'usage: <kadist.json>'
  sys.exit(-1)
else:
  load_data(sys.argv[1])
