from gensim import corpora, models, similarities
from gensim.models import hdpmodel, ldamodel, lsimodel
import sys
import codecs
from nltk.corpus import stopwords

stoplist = stopwords.words('english')
stoplist.extend(["also","said","work","one","two","three"])

with codecs.open(sys.argv[1], 'r', encoding='utf-8') as docs:

  documents = docs.readlines()
  dictionary = corpora.Dictionary(text.lower().split() for text in documents)
  stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
  once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq == 3]
  dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
  dictionary.compactify()

  corpus = [dictionary.doc2bow(line.lower().split()) for line in documents]

  tfidf = models.TfidfModel(corpus, normalize=True)

  corpus_tfidf = tfidf[corpus]

  print 'LDA', '*'*50
  lda = ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=200)
  for topic in lda.show_topics(num_topics=20, num_words=10, log=False, formatted=False):
    print [x[1] for x in topic]

  print 'LSI', '*'*50
  lsi = lsimodel.LsiModel(corpus, id2word=dictionary, num_topics=50)
  for topic in lsi.show_topics(num_topics=20, num_words=10, log=False, formatted=False):
    print [x[1] for x in topic]

  print 'HDP', '*'*50
  hdp = hdpmodel.HdpModel(corpus, id2word=dictionary)
  for count, topic in hdp.show_topics(topics=-1, topn=10, log=False, formatted=False):
    print count, [x[0] for x in topic]
