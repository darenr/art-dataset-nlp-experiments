from alchemyapi.alchemyapi import AlchemyAPI
import json
import unicodecsv
import sys
from collections import OrderedDict

alchemyapi = AlchemyAPI()

results = []

with open('MOMA3k.csv', 'rb') as in_csv:
  stop = False
  rows = unicodecsv.reader(in_csv, encoding='utf-8')
  fieldnames = rows.next()

  for line in rows:
    m = OrderedDict([(k,line[i]) for i,k in enumerate(fieldnames)])
    if not stop:
      txt = m['ExtraText'].encode('ascii', 'ignore').strip()
      print 'tagging:', txt
      concepts = alchemyapi.concepts('text', txt)
      if concepts['status'] == 'OK':
        m['AlchemyConcepts'] = ', '.join(["{0} ({1})".format(k['text'].encode('ascii', 'ignore'), k['relevance']) for k in concepts['concepts']])
      else:
        print(concepts)
        stop = True
    results.append(m)
  in_csv.close()

with open('MOMA3k.csv', 'wb') as out_csv:
  output = unicodecsv.DictWriter(out_csv, fieldnames=fieldnames, lineterminator='\n', quoting=unicodecsv.QUOTE_ALL)
  output.writerow(dict((fn,fn) for fn in fieldnames))
  for row in results:
    output.writerow(row)
    out_csv.flush()
