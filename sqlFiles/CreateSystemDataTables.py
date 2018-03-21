#! usr/bin/python3.5

#####################################################################################
#     built the tables needed for the system created data
#####################################################################################
import sqlite3

def createTests(connection):
    connection.execute('CREATE TABLE IF NOT EXISTS tests(testID INTEGER NOT NULL,\
                             date   DATETIME,\
                             duration INTEGER,\
                             reportLocation  TEXT,\
                             configID INTEGER NOT NULL,\
                             PRIMARY KEY (testID),\
                             FOREIGN KEY (configID) REFERENCES configuration(configID))')

       
def createMethods(connection):
    connection.execute("CREATE TABLE IF NOT EXISTS methods(name TEXT NOT NULL,\
                                testID  INTEGER NOT NULL,\
                                FOREIGN KEY (testID) REFERENCES tests(testID))")

def createWebsiteList(connection):
    connection.execute("CREATE TABLE IF NOT EXISTS websiteList(siteNo TEXT NOT NULL,\
                               URL TEXT NOT NULL,\
                               PRIMARY KEY (siteNo))")

def createWebsiteSamples(connection):
    connection.execute("CREATE TABLE IF NOT EXISTS websiteSamples(siteID INTEGER NOT NULL,\
                               URL BLOB NOT NULL,\
                               type TEXT ,\
                               testpg TEXT,\
                               testID INTEGER NOT NULL,\
                               PRIMARY KEY (siteID),\
                               FOREIGN KEY (testID) REFERENCES tests(testID))") 

    
def createWebpages(connection):
    connection.execute("CREATE TABLE IF NOT EXISTS webpages(pageID INTEGER NOT NULL,\
                               URL BLOB NOT NULL,\
                               timeRetrieved DATETIME,\
                               rawData BLOB ,\
                               pageType TEXT,\
                               siteID INTEGER NOT NULL,\
                               PRIMARY KEY (pageID),\
                               FOREIGN KEY (siteID) REFERENCES websiteSamples(siteID))")
    
    
def createDisplay(connection):
    connection.execute("CREATE TABLE IF NOT EXISTS display(displayID INTEGER NOT NULL,\
                               URL BLOB,\
                               fileType TEXT NOT NULL,\
                               timeRetrieved DATETIME,\
                               rawData BLOB ,\
                               pgID INTEGER NOT NULL,\
                               PRIMARY KEY (displayID),\
                               FOREIGN KEY (pgID) references webpages(pageID))")

    
def createTags(connection):
    connection.execute("CREATE TABLE IF NOT EXISTS tags(pageID INTEGER NOT NULL,\
                               tag BLOB NOT NULL,\
                               tagNo INTEGER NOT NULL,\
                               FOREIGN KEY(pageID) REFERENCES webpages(pageID))")


def createContent(connection):
    connection.execute("CREATE TABLE IF NOT EXISTS content(pageID INTEGER NOT NULL,\
                               content BLOB NOT NULL,\
                               contentNo INTEGER NOT NULL,\
                               FOREIGN KEY(pageID) REFERENCES webpages(pageID))")

def createTagcount(connection):
    connection.execute("""CREATE TABLE IF NOT EXISTS tagCount(pageID INtEGER NOT NULL,\
                               tagString BLOB NOT NULL,\
                               count INTEGER NOT NULL,\
                               FOREIGN KEY(pageID) REFERENCES webpages(pageID))""")
def createNgrams(connection):
    connection.execute("""CREATE TABLE IF NOT EXISTS Ngrams(pageID INtEGER NOT NULL,\
                               Ngram INTEGER NOT NULL,\
                               tagString BLOB NOT NULL,\
                               count INTEGER NOT NULL,\
                               FOREIGN KEY(pageID) REFERENCES webpages(pageID))""")

def createsiteStats(connection):
    connection.execute("""CREATE TABLE IF NOT EXISTS siteStats(siteID INTEGER NOT NULL,\
                               method TEXT NOT NULL,\
                               tagString    BLOB NOT NULL,\
                               mean   FLOAT,
                               SD     FLOAT)""")

def createResults(connection):
    connection.execute("""CREATE TABLE IF NOT EXISTS results(testID INTEGER NOT NULL,\
                               siteID INTEGER NOT NULL,\
                               accuracy FLOAT  NOT NULL)""")


def createPageResults(connection):
    connection.execute("""CREATE TABLE IF NOT EXISTS pageResults(siteID INTEGER NOT NULL,\
                               pageID INTEGER NOT NULL,\
                               result FLOAT NOT NULL)""")

    
def createTagLists(connection):
    connection.execute("""CREATE TABLE IF NOT EXISTS tagLists(testID INTEGER NOT NULL,\
                               siteID INTEGER NOT NULL,\
                               tagList BLOB, \
                               accuracy FLOAT)""")
                        


def createSignatures(connection):
    connection.execute("""CREATE TABLE IF NOT EXISTS signatures(testID INTEGER NOT NULL,\
                               siteID INTEGER NOT NULL,\
                               solution BLOB NOT NULL,\
                               rank FLOAT NOT NULL,\
                               accuracy FLOAT NOT NULL )""")
    

def createNetworkResults(connection):
    connection.execute("""CREATE TABLE IF NOT EXISTS networkResults(testID INTEGER NOT NULL,\
                               siteID INTEGER NOT NULL,\
                               error  INTEGER NOT NULL)""")

    
def createTables(connection):

   createTests(connection)
   createMethods(connection)
   createWebsiteList(connection)
   createWebsiteSamples(connection)
   createDisplay(connection)
   createWebpages(connection)
   createTags(connection)
   createContent(connection)
   createTagcount(connection)
   createNgrams(connection)
   createsiteStats(connection)
   createResults(connection)
   createPageResults(connection)
   createTagLists(connection)
   createSignatures(connection)
   createNetworkResults(connection)
   

connection = sqlite3.connect('../database/csci491')
createTables(connection)
connection.commit()
connection.close()
