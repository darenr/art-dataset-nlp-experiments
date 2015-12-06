from nltk.corpus import wordnet

ss = ['transience.n.01', 'eerie.s.01', 'landscape.n.03', 'photographic_print.n.01', 'isolation.n.03', 'darkness.n.05', 'impermanence.n.01']

for s in ss:
  print s, wordnet.synset(s).hypernyms()

print wordnet.synset('site.n.01').hyponyms()
