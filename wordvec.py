import os
from gensim.models import Word2Vec

model = Word2Vec.load_word2vec_format(os.environ['HOME'] + "/models/glove.42B.300d.txt", binary=False)

for word in ["childhood", "loss", "memory"]:
  if word in model:
    print word, model.most_similar(word)
