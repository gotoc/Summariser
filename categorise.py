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

import sqlite3
import math
import sys

def buildDB():
    conn = sqlite3.connect("words.db")
    c = conn.cursor()
    
    c.executescript("""
        CREATE TABLE words (
            word_id INTEGER PRIMARY KEY NOT NULL,
            word TEXT UNIQUE NOT NULL,
            sport INTEGER NOT NULL,
            not_sport INTEGER NOT NULL);
        CREATE TABLE vars (
            name TEXT PRIMARY KEY NOT NULL,
            value INTEGER);
        INSERT INTO vars (name, value) VALUES ("Total articles", 0);
        INSERT INTO vars (name, value) VALUES ("Total sport", 0);
        INSERT INTO vars (name, value) VALUES ("Total not sport", 0);""")
    
    conn.commit()
    conn.close()

def insert_words(words, category):
    """Insert words into database if not already existing,
    then increment the correct column"""
    
    #Turn list of words into tuple
    words = tuple([(i,) for i in words])
    
    conn = sqlite3.connect("words.db")
    c = conn.cursor()
    
    c.executemany("INSERT OR IGNORE INTO words (word, sport, not_sport) VALUES (?, 0, 0)", words)
    
    if category == "y":
        c.executemany("UPDATE words SET sport = (sport + 1) WHERE word = ?", words)
        c.execute("UPDATE vars SET value = (value + 1) WHERE name == \"sport\"")
    if category == "n":
        c.executemany("UPDATE words SET not_sport = (not_sport + 1) WHERE word = ?", words)
        c.execute("UPDATE vars SET value = (value + 1) WHERE name == \"not sport\"")
    
    c.execute("UPDATE vars SET value = (value + 1) WHERE name in ('Total articles', 'Total sports', 'Total not sports')")
    
    
    conn.commit()
    conn.close()

def get_word_probabilies():
    #Turn list of words into tuple
    conn = sqlite3.connect("words.db")
    c = conn.cursor()
    
    c.execute("SELECT * FROM words")
    all_words = list(c.fetchall())
    c.execute("SELECT value FROM vars WHERE name in ('Total articles', 'Total sport', 'Total not sport')")
    results = list(c.fetchall())
    total = results[0][0]
    sports_total = results[1][0]
    not_sports_total = results[2][0]
    
    conn.commit()
    conn.close()
    
    return all_words, total, sports_total, not_sports_total

if "-buildDB" in sys.argv:
    buildDB()
elif "-guess" in sys.argv:
    filepath = "../articles/article1.txt"
    
    with open(filepath, "r") as article_file:
        article = article_file.read().decode("utf-8")
        
        article = article.encode("ascii", errors='ignore')
        article = article.replace(".","").replace("?","").replace("!","").replace(",","")
        
        words = list(set(article.split()))
        
        all_words, total, sports_total, not_sports_total = get_word_probabilies()
        
        all_words_dict = {}
        for i in all_words:
            all_words_dict[i[1].lower()] = [float(i[2]), float(i[3])]
        
        #Bayesian bit
        
        n = 0
        for i in words:
            if i.lower() in all_words_dict:
                p_ws = all_words_dict[i.lower()][0] / sports_total
                p_wns = all_words_dict[i.lower()][1] / not_sports_total
                
                if p_ws != 0 and p_wns != 0:
                    p_i = p_ws / float(p_ws + p_wns)
                    
                    n += math.log(1-p_i) - math.log(p_i)
        
        p_s = 1 / (1 + math.e**n)
        
        n = 0
        for i in words:
            if i.lower() in all_words_dict:
                p_ws = all_words_dict[i.lower()][0] / sports_total
                p_wns = all_words_dict[i.lower()][1] / not_sports_total
                
                if p_ws != 0 and p_wns != 0:
                    p_i = p_wns / float(p_ws + p_wns)
                    
                    n += math.log(1-p_i) - math.log(p_i)
        
        p_ns = 1 / (1 + math.e**n)
        
        print p_s, p_ns
        
        if p_s > p_ns:
            print "Sport"
        else:
            print "Not sport"
        
else:
    #filepath = raw_input("Path to file: ")
    #category = raw_input("Is it a sports article? [Y/N] ")
    
    filepath = "../articles/article1.txt"
    category = "y"
    
    if category.lower() in ["y","n"]:
        with open(filepath, "r") as article_file:
            article = article_file.read().decode("utf-8")
            
            article = article.encode("ascii", errors='ignore')
            article = article.replace(".","").replace("?","").replace("!","").replace(",","")
            
            words = list(set(article.split()))
            
            insert_words(words, category)














