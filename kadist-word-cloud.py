from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS

d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d, 'unique_extra_files.txt')).read()

wc = WordCloud(background_color="white", max_words=100,
               width=700, height=500,
               stopwords=STOPWORDS.update(["said", "work","one","two","three"]))
# generate word cloud
wc.generate(text)

# store to file
wc.to_file(path.join(d, "moma-cloud.png"))
