from elasticsearch import Elasticsearch
import sys
import urllib3

if len(sys.argv) == 1:
  url = 'http://localhost:9200'
else:
  url = sys.argv[1]
es = Elasticsearch([url])
  
print es.search(index="kadist", body={"query": {"match": {'title':'war'}}})

