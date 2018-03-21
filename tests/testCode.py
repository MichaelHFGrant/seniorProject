#! /usr/bin/python3.5

import sqlite3, GeneralProcesses, BeautifulSoup


# ratio of tags described by rExpr to total number of tags
def trait1(connection,pageID,rExpr):
    query = "SELECT tags FROM tags WHERE pageID = ':pageID'"
    tagList = connection.query(query,(pageID))
    tags = tagList.split(',')
    tagCount = 0
    
    for tag in tags:
        if re.match(rExpr,tag):
            tagCount +=1
    return tagCount / len(tags)



# how many dev tags (how much the site is divided into sections)
def trait2(connection,pageID,rExpr):
    query = "SELECT content FROM content WHERE pageID = ':pageID'"
    tagList = connection.query(query,(pageID))
    tags = tagList.split(',')
    tagCount = 0
    
    for tag in tags:
        if re.match(rExpr,tag):
            tagCount +=1
    return tagCount



# how many different tags where used
def trait3(connection.pageID,rExper):
    query = "SELECT tags FROM tags WHERE pageID = ':pageID'"
    tagList = connection.query(query,(pageID))
    tags = tagList.split(',')
    tagCount = 0
    tagDict ={}

    strippedHTML = '\n'.join(tags)
    soupHTML = BeautifulSoup(strippedHTML,'thml.parser')

    
    return len(tagDict)

    
