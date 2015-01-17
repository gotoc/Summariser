"""
    Tries to make a best guess of what category the news
    article would best fit into based on the words
    contained.
    
    This will use a naive Bayesian filter in order to learn
    what category various articles belong in, so it will
    have to be trained before it is able to make any
    sensible guesses.
    
    A quick recap. A Bayesian filter works as follows:
    
    P(A|B) = (P(B|A)P(A)) / (P(B|A)P(A) + P(B|C)P(B))
    
    Where:
    P(A|B) is the probability it is in the category
    P(A)   is the probability it is in the category
    P(B|A) is the probability the word appears in
           other articles in the category
    P(B)   is the probability is is not in the category
    P(B|C) is the probability the word appears in
           other articles outside the category
    
    We then repeat this for all words in the article, and
    combine the probabilities to find the general
    probability the article belongs in that category.
"""


article = u""""""

article = article.encode("ascii", errors='ignore')

words = list(set(article.split()))

print words