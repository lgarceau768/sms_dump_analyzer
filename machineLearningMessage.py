import os, sys
from prettytable import *

# need to basically find commonalities in words / phrases

# will test on .txt file first
# open file
def readFile(allLines):
    with open('sample.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            allLines.append(line)

# now loop through all words in the list
def similarCheck(allLines):
    usedWords = []
    similar = []
    for i in allLines:
        words = i.replace('\n','').strip().split(' ')
        for word in words:
            # loop through every word and then check for more hits in the other lines
            if len(word) <= 2:
                continue
            if word not in usedWords:
                hits = 0
                for line in allLines:
                    if word in line:
                        hits+=1
                usedWords.append(word)
                if hits >= 10:
                    similar.append([word, hits])
    def second(val):
        return val[1]
    similar.sort(key = second, reverse = True)
    similarWords = PrettyTable()
    similarWords.field_names = ['Word', 'Hits']
    for word in similar:
        similarWords.add_row([word[0], word[1]])
    print(similarWords)


            




