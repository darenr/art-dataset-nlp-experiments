from nltk.corpus import wordnet
import itertools as IT
list1 = ["war"]
list2 = ["battle"]
def f(word1, word2):
    wordFromList1 = wordnet.synsets(word1)[0]
    wordFromList2 = wordnet.synsets(word2)[0]
    s = wordFromList1.wup_similarity(wordFromList2)
    return(wordFromList1.name, wordFromList2.name, wordFromList1.wup_similarity(wordFromList2))

for word1 in list1:
    similarities=(f(word1,word2) for word2 in list2)
    print(max(similarities, key=lambda x: x[2]))
