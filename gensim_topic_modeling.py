from gensim import corpora, models, similarities
from gensim.models import hdpmodel, ldamodel
import codecs
from nltk.corpus import stopwords

stoplist = stopwords.words('english')

with codecs.open('unique_extra_files.txt', 'r', encoding='utf-8') as docs:
  documents = docs.readlines()

  texts = [[word for word in document.lower().split() if word not in stoplist]
         for document in documents]

  '''
  all_tokens = sum(texts, [])
  tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
  texts = [[word for word in text if word not in tokens_once]
         for text in texts]
  '''

  dictionary = corpora.Dictionary(texts)
  corpus = [dictionary.doc2bow(text) for text in texts]

  tfidf = models.TfidfModel(corpus, normalize=True)

  corpus_tfidf = tfidf[corpus]

  print 'LDA', '*'*50
  lda = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=200)
  for topic in lda.show_topics(num_topics=20, num_words=10, log=False, formatted=False):
    print [x[1].encode('utf-8', 'ignore') for x in topic]
