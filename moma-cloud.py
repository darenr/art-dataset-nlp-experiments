from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt

from wordcloud import WordCloud, STOPWORDS

d = path.dirname(__file__)

# Read the whole text.
text = open(path.join(d, 'unique_extra_files.txt')).read()

wc = WordCloud(background_color="white", max_words=1000,
               width=800, height=600,
               stopwords=STOPWORDS.add("work"))
# generate word cloud
wc.generate(text)

# store to file
wc.to_file(path.join(d, "moma-cloud.png"))
