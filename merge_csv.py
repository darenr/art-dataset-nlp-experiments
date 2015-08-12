from __future__ import division
import unicodecsv
import sys
import codecs
import requests
import os
import time
import re
import random

results = []
preview = []

def enrich(m):
  r = re.search(r'\((\w+).*$', m.get('ArtistBio', '(Unknown,)'))
  if r:
    m['ArtistNationality'] = r.group(1).upper()

with open('Artworks.csv', 'rb') as in_csv:
  for m in unicodecsv.DictReader(in_csv, encoding = 'utf-8'):
    url = m['URL']
    oid = m['ObjectID']
    # augment with text processing
    enrich(m)

    # merge scraped extra text
    fname = os.path.join('extras', oid + '.txt')
    if os.path.isfile(fname):
      with open(fname) as f:
        m['HasExtraText'] = 'Y'
        m['ExtraText'] = unicode(f.read().replace('\n', ' ').replace('\r', ''), 'utf-8')
        preview.append(m)
    else :
      m['HasExtraText'] = 'N'
    results.append(m)

with open('MergedArtworks.csv', 'wb') as out_csv:
  wr = unicodecsv.DictWriter(out_csv,
    encoding = 'utf-8',
    quoting = unicodecsv.QUOTE_ALL,
    fieldnames = results[0].keys())
  wr.writeheader()
  for row in results:
    wr.writerow(row)

with open('MergedArtworksPreview.csv', 'wb') as out_csv:
  rand_smpl = [preview[i] for i in sorted(random.sample(xrange(len(preview)), 25))]
  wr = unicodecsv.DictWriter(out_csv,
    encoding = 'utf-8',
    quoting = unicodecsv.QUOTE_ALL,
    fieldnames = results[0].keys())
  wr.writeheader()
  for row in rand_smpl:
    wr.writerow(row)
