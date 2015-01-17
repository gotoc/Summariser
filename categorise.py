article = u""""""

article = article.encode("ascii", errors='ignore')

words = list(set(article.split()))

print words