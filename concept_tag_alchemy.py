from alchemyapi.alchemyapi import AlchemyAPI
import json
import unicodecsv

alchemyapi = AlchemyAPI()

results = []

with open('MOMA3k.csv', 'rb') as in_csv:
  for i, m in enumerate(unicodecsv.DictReader(in_csv, encoding='utf-8')):
    print i
    fieldnames = m.keys()
    fieldnames.extend(['AlchemyKeywords', 'AlchemyConcepts'])
    if not 'AlchemyConcepts' in m:
      txt = m['ExtraText'].encode('ascii', 'ignore')
      keywords = alchemyapi.keywords('text', txt)
      concepts = alchemyapi.concepts('text', txt)
      if keywords['status'] == 'OK' and concepts['status'] == 'OK':
        m['AlchemyKeywords'] = ', '.join(["{0} ({1})".format(k['text'].encode('ascii', 'ignore'), k['relevance']) 
          for k in keywords['keywords']])
        m['AlchemyConcepts'] = ', '.join(["{0} ({1})".format(k['text'].encode('ascii', 'ignore'), k['relevance']) 
          for k in concepts['concepts']])
      else:
        print('Error in concept tagging call: ', keywords['statusInfo'])
        break
      results.append(m)


with open('MOMA3k-tagged.csv', 'wb') as out_csv:
  output = unicodecsv.DictWriter(out_csv, fieldnames=fieldnames, quoting=unicodecsv.QUOTE_ALL)
  output.writerow(dict((fn,fn) for fn in fieldnames))
  for i, row in enumerate(results):
    output.writerow(row)
    if i % 100 == 0:
      out_csv.flush()
