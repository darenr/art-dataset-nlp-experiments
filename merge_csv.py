import unicodecsv
import sys
import codecs
import requests
import os
import time

results = []

with open('Artworks.csv', 'rb') as in_csv:
  for m in unicodecsv.DictReader(in_csv, encoding='utf-8'):
    url = m['URL']
    oid = m['ObjectID']
    fname = os.path.join('extras', oid + '.txt')
    if os.path.isfile(fname):
      with open(fname) as f:
        m['ExtraText'] = unicode(f.read().replace('\n', ' ').replace('\r', ''), 'utf-8')
    results.append(m)

with open('MergedArtworks.csv', 'wb') as out_csv:
  wr = unicodecsv.DictWriter(out_csv, encoding='utf-8', quoting=unicodecsv.QUOTE_ALL, fieldnames = results[0].keys())
  for m in results:
    wr.writerow(m)
