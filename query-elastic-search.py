from datetime import datetime
from elasticsearch import Elasticsearch
import json
import codecs
import sys
import datetime

es = Elasticsearch()

res = es.search(index="kadist", body={"query": {"fuzzy": {"minor_tags": "earthquake"}}})
print("Got %d Hits:" % res['hits']['total'])
for hit in res['hits']['hits']:
    print("%(id)d - [%(worktype)s] %(title)s" % hit["_source"])
