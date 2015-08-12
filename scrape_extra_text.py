import csv
import sys
import codecs
import requests
from bs4 import BeautifulSoup
import os
import time


def UnicodeDictReader():
    with open('Artworks.csv', 'rb') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            yield dict([(key, unicode(value, 'utf-8')) for key, value in row.iteritems()])


for m in UnicodeDictReader():
    url = m['URL']
    oid = m['ObjectID']

    fname = os.path.join('extras', oid + '.txt')
    if url and not os.path.isfile(fname):
        # time.sleep(1)
        r = requests.get(url)
        soup = BeautifulSoup(r.text)
        div = soup.find("div", {"class": "body-copy"})
        if div:
            txt = div.getText().encode('utf-8').strip()
            if txt and len(txt) > 200 and not txt.startswith('In order to effectively'):
                with open(fname, "w") as tf:
                    tf.write(txt)
                    print 'writing', fname, len(txt), 'bytes'
