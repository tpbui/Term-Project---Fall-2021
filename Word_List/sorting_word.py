import string
import random

def calculateDifficulty(s):
    dif = 0
    row = set()
    for letter in s:
        if letter in string.ascii_lowercase:
            if letter in "qazp":
                dif += 0.4
            if letter in "wsxol.":
                dif += 0.3
            if letter in "edcik,":
                dif += 0.2
            if letter in "rfvtgbyhnujm":
                dif += 0.1
    
        if letter in string.punctuation:
                dif += 0.5  
        if letter.isupper() == True:
                dif += 0.5
        if letter.isdigit() == True:
                dif += 0.5
        
    if len(s) == 1:
        dif += 0.5
    elif 2 <= len(s) <= 4:
        dif += 1
    elif 5 <= len(s) <= 6:
        dif += 1.5
    elif 7 <= len(s) <= 8:
        dif += 2
    elif len(s) >= 9:
        dif += 2.5
            
    return int(dif * 2)

#0-3:easy
#3-5:medium
#6-8:hard
#8 and more: supreme

def readFile(path):
    with open(path, "rt") as f:
        a = f.read()
        myWordList = a.split("\n")
        return myWordList[:-1]

def categorizingWord(path):
    wordList = readFile(path)
    for item in readFile(path):
        res = calculateDifficulty(item)
        if 0 <= res <= 3:
            with open("easy.txt", "a") as f:
                f.write(item)
                f.write("\n")
        elif 4 <= res <= 6:
            with open("medium.txt", "a") as f:
                f.write(item)
                f.write("\n")
        elif res > 7:
            with open("hard.txt", "a") as f:
                f.write(item)
                f.write("\n")
            
def categorizingFiles():
    lst = ["easy.txt", "medium.txt", "hard.txt"]
    for item in lst:
        file = open(item, 'w')
        file.close()
    categorizingWord("10k words.txt")

categorizingFiles()
