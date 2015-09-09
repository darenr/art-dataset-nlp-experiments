from datetime import datetime
from elasticsearch import Elasticsearch
import json
import codecs
import sys
import datetime

if len(sys.argv) != 2:
  print 'usage: <kadist.json>'
  sys.exit(-1)

es = Elasticsearch()


def load_data(index):
  if es.indices.exists(index=index):
    print es.indices.delete(index=index)
  print es.indices.create(index=index)

  with codecs.open(sys.argv[1], 'rb', 'utf-8') as f:
    kadist = json.loads(f.read())
    for m in kadist:
      # first change the tags to all be simple (no synsets)
      m['major_tags_wn'] = m['major_tags']
      m['minor_tags_wn'] = m['minor_tags']
      m['major_tags'] = [x.split('.')[0] for x in m['major_tags']]
      m['minor_tags'] = [x.split('.')[0] for x in m['minor_tags']]
      try:
        es.index(index=index, doc_type='kadist_art_collection', id=m['id'], body=m)
      except KeyboardInterrupt:
        raise
      except:
        print m



load_data('kadist')
