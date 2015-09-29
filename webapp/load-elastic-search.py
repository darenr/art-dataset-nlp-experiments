from elasticsearch import Elasticsearch
import json
import sys
import codecs
import urllib3
from textblob import TextBlob, Word

urllib3.disable_warnings()

def load_data(filename, es):
  index = 'kadist'
  doc_type = 'kadist_art_collection'
  if es.indices.exists(index=index):
    print es.indices.delete(index=index)

  # the analyzer settings
  analyzer_settings = {
    "analyzer": {
      "kadist_synonyms": {
        "tokenizer": "standard",
        "filter": [
          "standard",
          "asciifolding",
          "lowercase",
          "kadist_synonym_filter"
        ]
      }
    },
    "filter": {
      "kadist_synonym_filter": {
        "type": "synonym",
        "synonyms": [
          #
          # add synonyms here, they can be multi word. "leap,hop => jump"
          #
          "gender issues,feminism,gay=>gender",
          "cat=>kadist"
        ]
      }
    }
  }

  request_body = {
    "settings": {
      "number_of_shards": 1,
      "number_of_replicas": 0,
      "analysis": analyzer_settings
    }
  }

  print es.indices.create(index=index, body=request_body)

  schema = {
    'mappings': {
      doc_type: {
        "properties": {
          "worktype": {
            "store": "true",
            "type": "string",
            "term_vector": "yes",
            "index": "not_analyzed"
          },
          "collection": {
            "store": "true",
            "type": "string",
            "term_vector": "yes",
            "search_analyzer": "kadist_synonyms"
          },
          "decade": {
            "store": "true",
            "type": "string",
            "term_vector": "yes",
            "index": "not_analyzed"
          },
          "major_tags": {
            "store": "true",
            "type": "string",
            "term_vector": "yes",
            "index": "not_analyzed"
          },
          "minor_tags": {
            "store": "true",
            "type": "string",
            "term_vector": "yes",
            "index": "not_analyzed"
          },
          "artist_name": {
            "store": "true",
            "type": "string",
            "term_vector": "yes",
            "index": "not_analyzed"
          },
          "id": {
            "store": "true",
            "type": "string",
            "term_vector": "yes",
            "index": "not_analyzed"
          },
          "imgurl": {
            "store": "true",
            "type": "string",
            "stored": "yes",
            "index": "no"
          },
          "description": {
            "store": "true",
            "type": "string",
            "search_analyzer": "kadist_synonyms"
          },
          "artist_description": {
            "store": "true",
            "type": "string",
            "search_analyzer": "kadist_synonyms"
          }
        }
      }
    }
  }

  print es.indices.put_mapping(index=index, doc_type=doc_type, body=schema['mappings'])

  with codecs.open(filename, 'rb', 'utf-8') as f:
    kadist = json.loads(f.read())
    for m in kadist:
      if 'imgurl' in m and m['imgurl']:
        m['imgurl'] = m['imgurl'].split('?')[0]

      if len(m['major_tags']) or len(m['minor_tags']):
        m['mlt_tags'] = ' '.join([x.replace('.', '') for x in m['major_tags'] + m['minor_tags']])
      else:
        blob = TextBlob(' '.join([m['artist_name'], m['description']]))
        m['mlt_tags'] = ' '.join([x for x in blob.noun_phrases if blob.noun_phrases.count(x) > 0])

      m['collection'] = 'Kadist'
      m['decade'] = str(int(m['year'] / 10) * 10) + "s" if m['year'] else '0'

      try:
        es.index(index=index, doc_type=doc_type, id=m['id'], body=m)
      except KeyboardInterrupt:
        raise
      except:
        print m


if len(sys.argv) != 3 and sys.argv[2] in ['dev', 'prod']:
  print 'usage: <kadist.json> <dev|prod>'
  sys.exit(-1)
else:
  if sys.argv[2] == 'dev':
    print 'loading localhost:9200 elasticsearch'
    es = Elasticsearch(['http://localhost:9200'])
  else:
    es = Elasticsearch(['https://tcw4l779:9xy6x6d2vg9u6f83@dogwood-2734599.us-east-1.bonsai.io'])
  load_data(filename=sys.argv[1], es=es)
