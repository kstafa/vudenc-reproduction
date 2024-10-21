from gensim.models import Word2Vec

# Load the model
model = Word2Vec.load('w2v/word2vec_withString10-1-5.model')

# Find similar words
similar_words = model.wv.most_similar("if")
print(similar_words)
