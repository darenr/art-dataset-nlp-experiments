import os
from gensim.models import Word2Vec

model = Word2Vec.load_word2vec_format(os.environ['HOME'] + "/models/en_deps_300D_words.model")

for word in ["symbology", "dyslexia", "Language", "tactility", "communication", "tautology", "braille", "sight", "equations"]:
  if word in model:
    print word, model.most_similar(word)
