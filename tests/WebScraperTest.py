#! usr/bin/python3.5

import urllib, re, GeneralProcesses, WebScraper, sqlite3,bs4

def testFileRequest(reExp):


    for line in Fhandle:
        line = line.strip()
        print(line)
        (URL,  correctAnswer) = line.split()
        valid = WebScraper.fileRequest(URL,reExp)
        print(valid)
   #     print("correct answer: ",correctAnswer,"recieved answer: ",valid)
        return valid

def testIntermediateParser(connection):
    Fhandle = open("tests/IntermediateParser.txt")
    htmlFile = open("data/html.txt",'r')
    html = htmlFile.read()
    print(html)
#    for line in Fhandle:
 #       WebScraper.intermediateParser(connection,line[0],html,line[1])














def mainTest():
    Fhandle = open("tests/Webscraper.txt","r")
    testID = 1
    connection = GeneralProcesses.sql()

    for line in Fhandle:
        line = line.strip()
        (URL,CorrectAnswer)= line.split()
###        html = WebScraper.webScraper(connection,testID,URL,siteID)

#        print(html)
    connection.printAll(testID)
    connection.commit(connection)
    connection.close(connection)

mainTest()
        
