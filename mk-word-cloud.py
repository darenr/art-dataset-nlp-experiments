from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import sys
from nltk.corpus import stopwords

stoplist_en = stopwords.words('english')
stoplist_fr = stopwords.words('french')

stoplist_fr.extend(["les", "comme"])
stoplist_en.extend(["u", "untitled", "like", "also", "said", "work", "one", "two", "three"])

if len(sys.argv) < 3:
  print "usage <text corpus> <image output>"
  sys.exit(-1)

from wordcloud import WordCloud

d = path.dirname(__file__)

# Read the whole text.

text = open(path.join(d, sys.argv[1])).read()

wc = WordCloud(background_color="white", max_words=100,
               width=700, height=500,
               stopwords=stoplist_en+stoplist_fr)
# generate word cloud
wc.generate(text)

# store to file
wc.to_file(path.join(d, sys.argv[2]))
