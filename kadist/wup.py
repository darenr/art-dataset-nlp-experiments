from nltk.corpus import wordnet
import json
import codecs
import sys
import time

major_weight = 1.0
minor_weight = 0.7
similarity_threshold = 0.7

def fn(ss1, ss2):
  return (ss1.name(), ss2.name(), ss1.wup_similarity(ss2))

if len(sys.argv) != 3:
  print 'usage <seed synset> <kadist.json>'
  sys.exit(-1)
else:
  candidates = []

  source = wordnet.synset(sys.argv[1])

  with codecs.open(sys.argv[2], 'rb', 'utf-8') as f:
    kadist = json.loads(f.read())
    for m in kadist:
      if m['major_tags']:
        candidates += [wordnet.synset(tag) for tag in m['major_tags'] if '.n.' in tag]
      if m['minor_tags']:
        candidates += [wordnet.synset(tag) for tag in m['minor_tags'] if '.n.' in tag ]

  start = time.time()
  print 'starting similarity calculations'

  similarities = (fn(source, candidate) for candidate in set([c for c in candidates if c != source]))
  print(sorted( (sim for sim in similarities if sim[2] >= similarity_threshold), key=lambda x: x[2]))

  print source.name(), 'occurs as a tag', len([tag for tag in candidates if tag == source]),'times'
  print 'number lookups', len(candidates), 'duration', time.time()-start

