from datetime import datetime
from elasticsearch import Elasticsearch
import json
import codecs
import sys
import datetime
from textblob import TextBlob

if len(sys.argv) != 2:
  print 'usage: <kadist.json>'
  sys.exit(-1)

es = Elasticsearch()


def load_data(index):
  doc_type = 'kadist_art_collection'
  if es.indices.exists(index=index):
    print es.indices.delete(index=index)

  request_body = {
    "settings" : {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
  }

  print es.indices.create(index=index, body = request_body)

  schema = {
        'mappings': {
          doc_type: {
            "properties" : {
              "worktype" : {
                "type" :    "string",
                "term_vector" : "yes",
                "index":    "not_analyzed"
              },
              "major_tags" : {
                "type" :    "string",
                "term_vector" : "yes",
                "index":    "not_analyzed"
              },
              "minor_tags" : {
                "type" :    "string",
                "term_vector" : "yes",
                "index":    "not_analyzed"
              },
              "artist_name" : {
                "type" :    "string",
                "term_vector" : "yes",
                "index":    "not_analyzed"
              },
              "id" : {
                "type" :    "string",
                "term_vector" : "yes",
                "index":    "not_analyzed"
              },
              "imgurl" : {
                "type" :    "string",
                "stored" : "yes",
                "index":    "no"
              },
              "year" : {
                "type" :    "string",
                "term_vector" : "yes",
                "index":    "not_analyzed"
              },              
            }
          }
        }
      }

  print es.indices.put_mapping(index=index, doc_type=doc_type, body=schema['mappings'] )

  with codecs.open(sys.argv[1], 'rb', 'utf-8') as f:
    kadist = json.loads(f.read())
    for m in kadist:
      if 'imgurl' in m and m['imgurl']:
        m['imgurl'] = m['imgurl'].split('?')[0]

      if len(m['major_tags']) or len(m['minor_tags']):
        m['mlt_tags'] = ' '.join([x.replace('.','') for x in m['major_tags']+m['minor_tags']])
      else:
        blob = TextBlob(' '.join([m['artist_name'], m['description']]))
        m['mlt_tags'] = ' '.join([x for x in blob.noun_phrases if blob.noun_phrases.count(x) > 0])


      m['collection'] = 'Kadist'

      try:
        es.index(index=index, doc_type=doc_type, id=m['id'], body=m)
      except KeyboardInterrupt:
        raise
      except:
        print m



load_data('kadist')
