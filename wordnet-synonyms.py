from nltk.corpus import wordnet as wn
from nltk.corpus.reader import NOUN


for word in ["symbology", "dyslexia", "Language", "tactility", "communication", "tautology", "braille", "sight", "equations", "run"]:
  for i, ss in enumerate(wn.synsets(word, NOUN)):
    
    print word, ', '.join([l.name().decode('utf-8') for l in ss.lemmas() if l.name() != word])
