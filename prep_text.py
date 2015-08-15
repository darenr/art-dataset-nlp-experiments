import sys
import codecs
from textblob import TextBlob

with codecs.open(sys.argv[1], 'r', encoding='utf-8') as docs:
  for doc in docs:
    blob = TextBlob(doc.encode("ascii", "ignore"))
    print ' '.join([x.replace(' ', '_') for x in blob.noun_phrases])
