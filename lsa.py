import logging, gensim, bz2
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

id2word = gensim.corpora.Dictionary.load_from_text('unique_extra_files.txt')
mm = gensim.corpora.MmCorpus('wiki_en_tfidf.mm')
print(mm)
lda = gensim.models.ldamodel.LdaModel(corpus=mm, id2word=id2word, num_topics=100, update_every=1, chunksize=10000, passes=1)
lda.print_topics(20)
