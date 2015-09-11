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
  doc_type = 'kadist_art_collection'
  if es.indices.exists(index=index):
    print es.indices.delete(index=index)
  print es.indices.create(index=index)

  schema = {
        'mappings': {
          doc_type: {
            "properties" : {
              "worktype" : {
                "type" :    "string",
                "index":    "not_analyzed"
              },
              "major_tags" : {
                "type" :    "string",
                "index":    "not_analyzed"
              },
              "minor_tags" : {
                "type" :    "string",
                "index":    "not_analyzed"
              },
              "artist_name" : {
                "type" :    "string",
                "index":    "not_analyzed"
              },
              "imgurl" : {
                "type" :    "string",
                "index":    "no"
              }
            }
          }
        }
      }

  print es.indices.put_mapping(index=index, doc_type=doc_type, body=schema['mappings'] )

  with codecs.open(sys.argv[1], 'rb', 'utf-8') as f:
    kadist = json.loads(f.read())
    for m in kadist:
      # first change the tags to all be simple (no synsets)
      try:
        es.index(index=index, doc_type=doc_type, id=m['id'], body=m)
      except KeyboardInterrupt:
        raise
      except:
        print m



load_data('kadist')
