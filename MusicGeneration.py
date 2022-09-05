#!/usr/bin/env python
# coding: utf-8

# In[5]:


from collections import defaultdict
import random
import os 
import pandas as pd


# In[8]:


#chords_file = "chordlab\The Beatles"
#files = os.listdir(chords_file)


# In[10]:


chords_file = "all chords"
chordsloc = os.listdir(chords_file)
'''
index = 0 
for i in chordsloc :
    dataframe = open(chords_file+"\\"+i)
    dataframe1 = pd.DataFrame(dataframe)
    dataframe1.to_csv('chordscsv\\'+str(index)+'.csv', 
                  index = None)
    index+=1

'''
# In[3]:


index = 0
chords = []
for i in chordsloc :
    df = pd.read_csv("chordscsv\\"+str(index)+'.csv')
    for i in df['0']:
        chords.append(i.split(' ')[2].replace('\n', ''))
    index+=1
    chords.append("#END#")
#print(chords)


# In[84]:


'''chords_file = "chords"
chordsloc = os.listdir(chords_file)
for i in chordsloc :
    with open(chords_file+"/"+i, 'r') as f:
        chords = [x.replace('\n', '') for x in f.readlines()]
    chords.append("#END#")
    print(chords)'''


# In[86]:


def calculate_probabilities(tokens, ngrams=2):
    probs = dict()
    for i in range(ngrams, len(tokens)-1):
        if tuple(tokens[i-ngrams:i]) not in probs:
            probs[tuple(tokens[i-ngrams:i])] = dict()
        
        if tokens[i] not in probs[tuple(tokens[i-ngrams:i])]:
            probs[tuple(tokens[i-ngrams:i])][tokens[i]] = 0
        probs[tuple(tokens[i-ngrams:i])][tokens[i]] += 1
    
    for node in probs:
        total = sum(probs[node].values()) + len(probs[node].values())
        for next_token in probs[node]:
            probs[node][next_token] = (probs[node][next_token] + 1) / total
        
    return probs


def random_walk(probs,  starting_chords=('F', 'G7'), chord_count=30,min_song_len = 10,ngrams=2):
    chords = list(starting_chords)
    for i in range(ngrams, chord_count):
        current = tuple(chords[i-ngrams:i])
        choice =  random.choices(list(probs[current].keys()),
                                 list(probs[current].values()))
        if (choice[0] == "#END#" ):

            if (len(chords)<min_song_len ):
                return random_walk(probs,starting_chords,chord_count,min_song_len,ngrams)

            else:
                return chords
        chords += choice
    return chords

ng = 2
probs = calculate_probabilities(chords,ng)
start = 0
while (True):
    start = random.choice(list(probs.keys()))
    if "#END#" not in start:
        break

print(random_walk(probs, starting_chords=start, chord_count=40,min_song_len = 10,ngrams=ng))





