from nltk.corpus import wordnet
import json
import codecs
import sys
import time

major_weight = 1.0
minor_weight = 0.8
similarity_threshold = 0.65

def fn(ss1, ss2, weight):
  similarity = ss1.wup_similarity(ss2)
  return (ss1, ss2, weight * similarity if similarity else 0 )

def isSynsetForm(s):
  return '.n.' in s or '.s.' in s or '.v.' in s

if len(sys.argv) != 3:
  print 'usage <seed synset> <kadist.json>'
  sys.exit(-1)
else:
  candidates = []

  source = wordnet.synset(sys.argv[1])

  tagged_works = 0

  with codecs.open(sys.argv[2], 'rb', 'utf-8') as f:
    kadist = json.loads(f.read())
    for m in kadist:
      if m['major_tags']:
        tagged_works += 1
        candidates += [(wordnet.synset(tag), major_weight) for tag in m['major_tags'] if isSynsetForm(tag)]
      if m['minor_tags']:
        candidates += [(wordnet.synset(tag), minor_weight) for tag in m['minor_tags'] if isSynsetForm(tag) ]

  start = time.time()
  print 'starting similarity calculations on', tagged_works, 'tagged works'

  similarities = (fn(source, candidate[0], candidate[1]) for candidate in set([c for c in candidates if c[0] != source]))
  for result in (sorted( (sim for sim in similarities if sim[2] >= similarity_threshold), key=lambda x: x[2])):
    print result[0].name(), result[1].name(), result[2]

  print source.name(), 'occurs as a tag', len([c for c in candidates if c[0] == source]),'times'
  print 'number lookups', len(candidates), 'duration', time.time()-start

