#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import unicodecsv
import sys
import codecs
import requests
import os
import time
import re
import random

class CSVMerger(object):

  def __init__(self):
    self.results = []

  def enrich(self, m):
    r = re.search(r'\((\w+).*$', m['ArtistBio'])
    if r:
      m['ArtistNationality'] = r.group(1).upper()


  def merge(self):
    with open('Artworks.csv', 'rb') as in_csv:
      for m in unicodecsv.DictReader(in_csv, encoding='utf-8'):
        url = m['URL']
        oid = m['ObjectID']

        # augment with text processing
        self.enrich(m)

        # merge scraped extra text
        fname = os.path.join('extras', oid + '.txt')
        if os.path.isfile(fname):
          with open(fname) as f:
            m['HasExtraText'] = 'Y'
            m['ExtraText'] = unicode(f.read().replace('\n', ' ').replace('\r', ''), 'utf-8')
        else:
          m['HasExtraText'] = 'N'

        self.results.append(m)

  def sample(self):
    filtered = [x for x in self.results if x['HasExtraText'] == 'Y' and x['CuratorApproved'] == 'Y' and x['DateAcquired'].startswith('2')]
    return [filtered[i] for i in sorted(random.sample(xrange(len(filtered)), 25))
            ]

  def save(self, fname, rows):
    fieldnames = self.results[0].keys()
    with open(fname, 'wb') as out_csv:
      wr = unicodecsv.DictWriter(out_csv, encoding='utf-8', quoting=unicodecsv.QUOTE_ALL, fieldnames=fieldnames)
      wr.writeheader()
      for row in rows:
        wr.writerow(row)


if __name__ == "__main__":
  merger = CSVMerger()
  merger.merge()
  merger.save('MergedArtworks.csv', merger.results)
  merger.save('MergedArtworksPreview.csv', merger.sample())
