import os
from gensim.models import Word2Vec
from sklearn.cluster import KMeans

model = Word2Vec.load_word2vec_format(os.environ['HOME'] + "/models/en_deps_300D_words.model")

# Set "k" (num_clusters) to be 1/5th of the vocabulary size, or an
# average of 5 words per cluster
word_vectors = model.syn0
num_clusters = word_vectors.shape[0] / 10

# Initalize a k-means object and use it to extract centroids
kmeans_clustering = KMeans( n_clusters = num_clusters )
idx = kmeans_clustering.fit_predict( word_vectors )

# Create a Word / Index dictionary, mapping each vocabulary word to
# a cluster number                                                                                            
word_centroid_map = dict(zip( model.index2word, idx ))

# For the first 10 clusters
for cluster in len(word_centroid_map.values()):
    words = []
    for i in xrange(0,len(word_centroid_map.values())):
        if( word_centroid_map.values()[i] == cluster ):
            words.append(word_centroid_map.keys()[i])
    print words
