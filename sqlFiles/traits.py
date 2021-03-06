#! usr/bin/python3.5

import sqlite3


def insertTraits(connection):


    testCode="""
# get all tags from the database for current page
query = "SELECT tag FROM tags WHERE pageID = "+str(pageID[0])
tags = connection.getAll(query) 
tagList = []
for tag in tags:
   strippedTag = re.search(r'<[a-zA-Z]+',tag[0])
   
   if strippedTag:
      if strippedTag.group() not in tagList:
         tagList.append(strippedTag.group())
         query = "SELECT count(tag) FROM tags WHERE pageID = "+str(pageID)+" AND tag like '"+strippedTag.group()+"%'"
         count = connection.getOne(query)
         query = "INSERT INTO tagCount(tagString,count,pageID) VALUES(:tagString,:count,:pageID)"
         connection.query(query,(strippedTag.group(),count[0],pageID))

        """
    RExp =""" r'<[a-z]+'"""
    cur = connection.execute("""select count(*) from traits""")
    traitID = int(cur.fetchone()[0])+1
    query = """INSERT INTO traits(traitID, RExp,testCode) VALUES(:traitID,:RExp,:testCode)"""
    connection.execute(query,(traitID,RExp,testCode))
    cur = connection.execute("""select * from traits""")
    print(cur.fetchall())

def insertRarePairs(connection):
    testCode ="""
result = connection.getOne("SELECT Ngram FROM traits WHERE traitID = 2")
N = int(result[0])
Tags = []
for Tag in tags:
    tagG = re.search(r'<[a-z]+',Tag[0])
    if tagG:
        tag = tagG.group()    
        Tags.append(tag)
if len(tags)< N:
    N = len(Tags)
Ngrams=[]
for d in range(N):
    dic = {}
    Ngrams.append(dic)
gram = ''
for c in range(len(Tags)):
    if c > 0:
        gram = gram +'_'+ Tags[c]
    else:
        gram = Tags[c]
        Ngrams[0][Tags[c]] = 1
    if len(gram.split('_')) >N:
        (head,gram) = gram.split('_',1)
    tempgram = gram
    for x in range(1,len(tempgram.split('_'))):
        if tempgram in Ngrams[len(tempgram.split('_'))-1]:
            Ngrams[len(tempgram.split('_'))-1][tempgram] +=1
        else:
            Ngrams[len(tempgram.split('_'))-1][tempgram] = 1
        (head,tail)=tempgram.split('_',1)
        if len(tail.split('_'))==1:
            if tail in Ngrams[0]:
                Ngrams[0][tail]+=1
            else:
                Ngrams[0][tail]=1
        tempgram = tail
query = "INSERT INTO Ngrams (pageID,Ngram, tagString,count) VALUES(:pageID, :count ,:tag,:tagCount)"
count=1
for grams in Ngrams:
    for tags in grams.keys():
         connection.query(query,(pageID,count,tags,grams[tags]))
    count+=1
"""
    RExp =""" r'<[a-z]+'"""
    N = 5
    cur = connection.execute("""select count(*) from traits""")
    traitID = int(cur.fetchone()[0])+1
    query = """INSERT INTO traits(traitID,Ngram, RExp,testCode) VALUES(:traitID,:N,:RExp,:testCode)"""
    connection.execute(query,(traitID,N,RExp,testCode))
    cur = connection.execute("""select * from traits""")
    print(cur.fetchall())

def insertTraitLists(connection):
    configID = 1
    traitID = 1
    query = """INSERT INTO traitList(\
                      traitID, method,args, condition, statTest, configID) VALUES(\
                      :traitID,:method,:arg,:condition,:statTest,:configID)"""
    method = "WriterInvariant"
    statTest = "tagCount"
    
    args=("<a","<div","<script","<li","<nav")
    for arg in args:
        condition = " AND tagString = '" + arg+"'"
        arguments = (traitID,method,arg,condition,statTest,configID)
        connection.execute(query,arguments)

    traitID = 2
    arg = 5
    method = "RarePairs"
    condition = ''
    statTest = "Ngrams"
    connection.execute(query,(traitID,method,arg,condition,statTest,configID))

def insertGeneticAlgorithm(connection):
    configID = 1
    traitID = 1
    query = """INSERT INTO traitList(\
                      traitID, method,args, condition, statTest, configID) VALUES(\
                      :traitID,:method,:arg,:condition,:statTest,:configID)"""
    method = "GeneticAlgorithm"
    statTest = "tagCount"
    tagQuery = """select distinct tagString FROM tagCount """
    curser = connection.execute(tagQuery)
    args = curser.fetchall()
    args=("<a","<div","<script","<li","<nav","<img","<meta","<title","<span","<footer","<input","<map","<style")
    for arg in args:

        
        condition = " AND tagString = '" + arg+"'"
        print(arg)
        arguments = (traitID,method,arg,condition,statTest,configID)
        connection.execute(query,arguments)

    traitID = 2
    arg = 5
    method = "RarePairs"
    condition = ''
    statTest = "Ngrams"
    connection.execute(query,(traitID,method,arg,condition,statTest,configID))





def insertNeuralNetworks(connection):
    configID = 1
    traitID = 1
    query = """INSERT INTO traitList(\
                      traitID, method,args, condition, statTest, configID) VALUES(\
                      :traitID,:method,:arg,:condition,:statTest,:configID)"""
    method = "NeuralNetwork"
    statTest = "tagCount"
    tagQuery = """select distinct tagString FROM tagCount """
    curser = connection.execute(tagQuery)
    args = curser.fetchall()
    args=("<a","<div","<script","<li","<nav","<img","<meta","<title","<span","<footer","<input","<map","<style")
    for arg in args:

        
        condition = " AND tagString = '" + arg+"'"
        print(arg)
        arguments = (traitID,method,arg,condition,statTest,configID)
        connection.execute(query,arguments)

    traitID = 2
    arg = 5
    method = "RarePairs"
    condition = ''
    statTest = "Ngrams"
    connection.execute(query,(traitID,method,arg,condition,statTest,configID))
                        
    
    

def main(connection):
    insertTraits(connection)
    insertRarePairs(connection)
    insertTraitLists(connection)
    insertGeneticAlgorithm(connection)
    insertNeuralNetworks(connection)
    connection.commit()
    



#connection = sqlite3.connect('../database/csci491')
#main(connection)
#connection.close()
