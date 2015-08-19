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

  if 'AlchemyKeywords' not in fieldnames:
    fieldnames.extend(['AlchemyKeywords'])
  if 'AlchemyConcepts' not in fieldnames:
    fieldnames.extend(['AlchemyConcepts'])

  for line in rows:
    m = OrderedDict([(k,line[i]) for i,k in enumerate(fieldnames)])
    if not stop and  not 'AlchemyConcepts' in m:
      txt = m['ExtraText'].encode('ascii', 'ignore')
      print 'tagging: "', txt, '"'
      keywords = alchemyapi.keywords('text', txt)
      concepts = alchemyapi.concepts('text', txt)
      if keywords['status'] == 'OK' and concepts['status'] == 'OK':
        m['AlchemyKeywords'] = ', '.join(["{0} ({1})".format(k['text'].encode('ascii', 'ignore'), k['relevance']) 
          for k in keywords['keywords']])
        m['AlchemyConcepts'] = ', '.join(["{0} ({1})".format(k['text'].encode('ascii', 'ignore'), k['relevance']) 
          for k in concepts['concepts']])
      else:
        print('Error in concept tagging call: ', keywords['status'])
        stop = True
    results.append(m)
  in_csv.close()

with open('MOMA3k.csv', 'wb') as out_csv:
  output = unicodecsv.DictWriter(out_csv, fieldnames=fieldnames, quoting=unicodecsv.QUOTE_ALL)
  output.writerow(dict((fn,fn) for fn in fieldnames))
  for i, row in enumerate(results):
    output.writerow(row)
    if i % 10 == 0:
      out_csv.flush()
