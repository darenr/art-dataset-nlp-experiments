from nltk.corpus import wordnet as wn
from nltk.corpus.reader import NOUN

print wn.synsets('gay')

for name in ["homosexual.n.01", "portraiture.n.01", "folk_art.n.01", "gender.n.02"]:
  syn = [l.name().decode('utf-8') for l in wn.synset(name).lemmas()]
 
  print name, ': ', ', '.join(set(syn))



