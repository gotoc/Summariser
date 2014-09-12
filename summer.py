article_title = "title"

article = """article"""

link_address = "link"

from articles import article_title, article, link_address
import random
import math
import re

OUTPUT_HTML = True

regex = "(?<=[.!?])\s"
stopwords = ["that","is","the","in","his","to","of","a","and","has","on","not",
             "he","said","had","it","-","by","be","as","this","who","or","for",
             "with","was","would","its","it's","he's","them","get","because",
             "in","at","this","your","news","could","i","those"]
minimumLength = 5

line_splits = article.split("\n")
sentences = []
for i in line_splits:
    if i != "":
        sentences += re.split(regex, i)


#Extract keywords
keywords = {}
for i in article_title.split():
    word = i.replace(",","").lower()
    if word not in stopwords:
        if word in keywords:
            keywords[word] += 1
        else:
            keywords[word] = 3

for i in sentences:
    for j in i.split():
        word = j.replace(",","").lower()
        if word not in stopwords:
            if word in keywords:
                keywords[word] += 0.5
            else:
                keywords[word] = 1

#Normalise keywords
import operator
max_val = float(sorted(keywords.iteritems(), key=operator.itemgetter(1))[-1][1])
for i in keywords:
    keywords[i] /= max_val

def score_length(sentence):
    if len(sentence.split()) < minimumLength:
        return 0
    return 1

def score_sentence(sentence, keywords):
    score = 0.0
    
    for i in sentence.split():
        if i.lower() in keywords and i.lower() not in stopwords:
            score += keywords[i.lower()]
    
    score /= len(sentence.split())
    
    lengthScore = score_length(sentence)
    
    score *= lengthScore
    
    return score

print sorted(keywords.iteritems(), key=operator.itemgetter(1))
#print keywords["not"]



scored_sentence = []
for i in sentences:
    scored_sentence.append([i,score_sentence(i, keywords)])

nice_sentences = sorted(scored_sentence, key=lambda x : x[1])[-3:][::-1]





print article_title
to_show = ""
for i in range(0,len(article_title)):
    to_show += "="
print to_show,"\n"

for i in range(0,3):
    print nice_sentences[i]


if OUTPUT_HTML:
    print "<div class='newsitem'>"
    print "    <h2>",article_title,"</h2>"
    print
    print "    <div class='newscontent'>"
    for i in nice_sentences:
        print "        <p>",i[0],"</p>"
        print 
    print "        <a href='",link_address,"'>Read more at BBC</a>"
    print "    </div>\n</div>"