#################################################################################
#    Author: Michael Grant
#    Date  : Jan 2018
#    Purpose:  To test the SQL package methods
#################################################################################

import SQLconnection

def insertWebsiteSampleTest(connection):
    print('Testing insertWebsiteSample')
    URL = "TEST.URL"
    siteID =  connection.getID('websiteSamples')
    Stype = "sample"
    testHTMLCode = open('testData/insertCases.txt','r')
    for line in testHTMLCode:
        pageID = connection.getID('webpages')
        connection.insertWebsiteSample(URL,pageID,line, siteID, Stype)
        result = connection.getAll("""SELECT * FROM webpages WHERE pageID = """+str(pageID))
        print(result,' ',line)
    testHTMLCode.close()

    
def getOneTest(connection):
    print('testing getOne')
    testGetOneQuery = open('testData/getOneCases.txt','r')
    for line in testGetOneQuery:
        result = connection.getOne(line)
        print(line,' ',result)
    testGetOneQuery.close()

def getAllTest(connection):
    print('Testing getAll')
    testGetAllQuery = open('testData/getAllCases.txt','r')
    for line in testGetAllQuery:
        result = connection.getOne(line)
        print(line,' ',result)
    testGetAllQuery.close()

def getIDTest(connection):
    print('Testing getID')
    testGetIDTables = open('testData/getIDTables.txt','r')
    for line in testGetIDTables:
        print(connection.getID(line))

def getConfigTest(connection):
    print('Testing getConfig')
    query = """SELECT testID FROM tests"""
    testIDs = connection.getAll(query)
    for testID in testIDs:
        print(connection.getConfig(testID[0]))

def getPageIDsTest(connection):
    print('Testing getPageIDs')
    pageIDs = connection.getPageIDs(1)
    for pageID in pageIDs:
        print(pageID)


def getSiteIDsTest(connection):
    print('Testing getSiteIDs')
    siteIDs = connection.getSiteIDs(1)
    for siteID in siteIDs:
        print(siteID)


def createTempTableTest(connection):
    print('Testing createTempTable')
    
def main():
    connection = SQLconnection.sql()
    insertWebsiteSampleTest(connection)
#    getOneTest(connection)
    getAllTest(connection)
    getIDTest(connection)
    getConfigTest(connection)
    getPageIDsTest(connection)
    getSiteIDsTest(connection)
    connection.close()
main()
    
