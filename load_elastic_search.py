from datetime import datetime
from elasticsearch import Elasticsearch
import json
import unicodecsv

es = Elasticsearch()

def load_data(index):
  if es.indices.exists(index=index):
    print es.indices.delete(index=index)
  print es.indices.create(index=index )

  with open('MergedArtworks.csv', 'rb') as in_csv:
    for m in unicodecsv.DictReader(in_csv, encoding='utf-8'):
      id = m['ObjectID']
      if not m['DateAcquired']:
        m['DateAcquired'] = '2015-01-01'
      try:
        es.index(index=index, doc_type='moma_art_collection', id=id, body=m)
      except KeyboardInterrupt:
        raise
      except:
        print m

load_data('moma')
