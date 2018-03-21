#! /usr/bin/python3.5

# experimental test code
import sqlite3,GeneralProcesses,re
connection = GeneralProcesses.sql()


s="""print("this is great")

"""
code = compile(s,"string","exec")
exec(code)

def strip(tag):
    newTag = ''
    newerTag = ''
    for letter in tag:
        if not (letter == '\\'):
            newTag = newTag+letter
    for letter in newTag:
        if not (letter == '\\'):
            newerTag = newerTag+letter
    
    return newerTag

pgID = 23
# trait1 code
# count the number of occurences of each tag over the entire webpage

RExp = r'<[a-z]+'
trait1Code = """
query = "SELECT tags FROM tags where pageID ="+ str(pageID[0])
   tagDict = {}
           for tag in connection.getAll(query):
               Tag = re.search(RExp,tag[0])
               if Tag:
                   if Tag.group() in tagDict:
                      tagDict[Tag.group()]+=1
                   else:
                      tagDict[Tag.group()] = 1
           print(tagDict)
           for tag in tagDict:
               query = "INSERT INTO tagcount(pageID,tag,count)\
                          VALUES(:pgID,:tag,:count)"
               connection.query(query,(str(pageID[0]),tag,tagDict[tag]))
        """
tags =['a','b','a','d','c','f','g','t','e','r','a','b','a','d','c','f','e']
N = 3
if len(tags)< N:
    N = len(tags)
Ngrams=[]
for d in range(N):
    dic = {}
    Ngrams.append(dic)
gram = ''
for c in range(len(tags)):
    if c > 0:
        gram = gram +'_'+ tags[c]
    else:
        gram = tags[c]
        Ngrams[0][tags[c]] = 1
    if len(gram.split('_')) >N:
        (head,gram) = gram.split('_',1)
    tempgram = gram
    for x in range(1,len(tempgram.split('_'))):
        if tempgram in Ngrams[len(tempgram.split('_'))-1]:
            Ngrams[len(tempgram.split('_'))-1][tempgram] +=1
        else:
            Ngrams[len(tempgram.split('_'))-1][tempgram] = 1
        (head,tail)=tempgram.split('_',1)
        if len(tail)==1:
            if tail in Ngrams[0]:
                Ngrams[0][tail]+=1
            else:
                Ngrams[0][tail]=1
        tempgram = tail

for x in Ngrams:
    print('\n')
for x in Ngrams:
    print(x)
    
