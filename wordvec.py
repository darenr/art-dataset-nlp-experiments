import os
from gensim.models import Word2Vec

model = Word2Vec.load_word2vec_format(os.environ['HOME'] + "/models/en_deps_300D_words.model")

for word in ["gender_issues", "lgbt", "gender", "light", "blackness"]:
  if word in model:
    print word, model.most_similar(word)
