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
      try:
        m['timestamp'] = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        es.index(index=index, doc_type='kadist_art_collection', id=m['id'], body=m)
      except KeyboardInterrupt:
        raise
      except:
        print m



load_data('kadist')
