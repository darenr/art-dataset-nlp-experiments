from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
import sys
import string
from nltk.corpus import stopwords

stoplist = stopwords.words('english')
stoplist.extend(stopwords.words('french'))

stoplist.extend(["cette", "made", "works", "image", "images", "les", "comme"])
stoplist.extend(["photograph", "photographer", "film", "untitled", "series", "artist"])
stoplist.extend(["photographs", "like", "also", "said", "work", "one", "two", "three"])
stoplist.extend(list(string.ascii_lowercase))

if len(sys.argv) < 3:
  print "usage <text corpus> <image output>"
  sys.exit(-1)

from wordcloud import WordCloud

d = path.dirname(__file__)

# Read the whole text.

text = open(path.join(d, sys.argv[1])).read()

wc = WordCloud(background_color="white", max_words=400,
               width=960, height=800,
               stopwords=stoplist)
# generate word cloud
wc.generate(text)

# store to file
wc.to_file(path.join(d, sys.argv[2]))
