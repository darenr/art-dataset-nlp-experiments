from textblob.en.np_extractors import ConllExtractor
from textblob import Blobber
from nltk.corpus import stopwords

stoplist = stopwords.words('english')
stoplist.extend(stopwords.words('french'))

stoplist.extend(["cette", "made", "works", "image", "images", "les", "comme"])
stoplist.extend(["photograph", "photographer", "film", "untitled", "series", "artist"])
stoplist.extend(["photographs", "like", "also", "said", "work", "one", "two", "three"])
stoplist.extend(["something", "often", "another", "used", "history", "time", "other"])


tb = Blobber(np_extractor=ConllExtractor()) 
b = tb('''An eerie feeling of deja vu. The two pieces in the Kadist Collection depict foggy landscapes, one at dawn, the other at nighttime. Both dimly lit scenes are dominated by an eerie feeling. Taken by a road, these painterly photographs suggest the uncanny character of the transient. Deeply interested in the topic of housing in the United States, Todd Hido's large, colored photographs of American suburbia emphasize feelings of isolation and anonymity. Heavily influenced by Larry Sultan's work, Hido's images have a very narrative, almost cinematic quality to them. Northern Californian fog frequently recurs in his photographs has become one of his most recognizable trademarks.''')



tags = b.tags
for i,t in enumerate(tags):
  if t[1].startswith('NN'):
    print t
