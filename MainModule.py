#! /usr/bin/python3.5
########################################################################################
# Title:          Main Module 
# Author:         Michael Grant
# Date:           Sept 2017
# Description:    Controls the timing and communication between the other system modules
# Arguments:      None. System will prompt user for needed input
# Sub-processes:  Webscraper, Parsing, Data-Manipulaton, Report, timer, websiteAquisition
########################################################################################


import Parser, WebScraper, DataManipulation, Presentation, GeneralProcesses, tests
import sqlite3, random 

########################################################################################
# Title:         WebsiteAquisition 
# Author:        Michael Grant   
# Date:          Sept 2017
# Description:   Accesses the Database and returns a list of available website URL's
# Arguments:     database connecton, testID
# Sub-processes: none
# Return Value:  Success or error message
########################################################################################

def websiteAquisition(connection,testID):
   print("This is the websiteAquisiton process")
   websites = dict()
   siteID = 0
   
   query = "SELECT configID FROM tests WHERE testID =" + str(testID)
   result = connection.getOne(query)
   configID = result[0]
   query = "SELECT websiteSampleSize, webpageSampleSize FROM samples\
                                 WHERE configID = " + str(configID)
   result = connection.getOne(query)
   websiteSampleSize = result[0]
   webpageSampleSize = result[1]
   query = "SELECT COUNT(*) FROM websiteList"
   result = connection.getOne(query)
   maxSample = int(result[0])
   websites = random.sample(range(1,maxSample),websiteSampleSize)
   print(websites)
   return websites

def websiteDataCollection(connection,sampleSize,internalLinks,siteID,testID):
   print("This is WebsiteCollection")
   random.seed()
   loopQuery = """ SELECT count(*) FROM webpages WHERE siteID = """ + str(siteID)
   usedLinks =[]
   potentialLinks =[]
   
   while connection.getOne(loopQuery)[0] < sampleSize:
      if internalLinks:
         for link in internalLinks:
            if link not in potentialLinks:
               if link not in usedLinks:
                  potentialLinks.append(link)
      internalLinks =[]
      while not internalLinks:
         urlIndex = random.randint(0,len(potentialLinks)-1)
         usedLinks.append(urlIndex)
         URL = potentialLinks[urlIndex]
         del potentialLinks[urlIndex]
         # request the webpage
         internalLinks = WebScraper.webScraper(connection,testID,URL,siteID)


   
def userInput(connection,configID):

   testID = None
   UserInput = input("Enter the method or methods to use separated with a space: ")
   methods = UserInput.split()
   print(methods)
   for method in methods:
      print(method)
      if (method == 'RarePairs' or method == 'WriterInvariant' or \
          method == 'GeneticAlgorithm' or method == 'NeuralNetwork'):
         testID = connection.getID('tests')
         query = "INSERT INTO tests(testID,configID) VALUES(:testID, :configID)"
         connection.query(query,(testID,configID))
         query = "INSERT INTO methods(name,testID)\
                                 values(:method,:testID)"
         connection.query(query,(method,testID))
      else:
         print("User Input Error")
   return testID

                
      
def mainModule():
   
######################################################################################
#  System Init
######################################################################################
   
   testing = 'false'
   print("This is the Main Module")
   status = 'false'
   controlFlag = 'true'
   configID = 1
   testID = None

   random.seed()
   internalLinks=[]
   

   connection = GeneralProcesses.sql()

######################################################################################
#            Main program loop
######################################################################################


   while (controlFlag == 'true'):
      while not testID:
         testID = userInput(connection,configID)
      cue = websiteAquisition(connection,testID)

   # get configuraton details for sample size
      query = "SELECT * FROM samples WHERE configID = " + str(configID)
      result = connection.getOne(query)
      websiteSampleSize = int(result[0])
      webpageSampleSize = int(result[1])
      redherringSize = int(result[2])
       # choose the redherrings
      redHerrings = random.sample(cue,redherringSize)
      print(redHerrings)
      for siteNo in cue:
         internalLinks = []
         query = "SELECT URL FROM websiteList WHERE siteNo = '" + str(siteNo) +"'"
         result = connection.getOne(query)
         URL = result[0]
         print("the siteURL is: ",URL)
         # get a siteID for the new websiteSample
         siteID = connection.getID('websiteSamples')
         query = """INSERT INTO websiteSamples (siteID,URL,testID) VALUES (:siteID,:URL,:testID)"""
         connection.query(query,(str(siteID),URL,str(testID)))
         while not internalLinks:
            internalLinks = WebScraper.webScraper(connection,testID,URL,siteID)
            if not internalLinks:
               print("no internal Links")
               # no internal links maybe 404 error or no links either way need a new website
               # pop siteNo from cue
               # drop the database entries for this site
               query = """SELECT pageID FROM webpages WHERE siteID = """+str(siteID)
               pageID = connection.getOne(query)
               query = """DELETE FROM webpages WHERE siteID = """+str(siteID)
               connection.getOne(query)
               
               if pageID:
                  query = """DELETE FROM display  WHERE pgID = """+str(pageID[0])
                  connection.getOne(query)
                  query = """DELETE FROM tags  WHERE pageID = """+str(pageID[0])
                  connection.getOne(query)
                  query = """DELETE FROM content  WHERE pageID = """+str(pageID[0])
                  connection.getOne(query)
               query = """SELECT COUNT(*) FROM websiteList"""
               result = connection.getOne(query)
               maxSample = int(result[0])
               newSiteNo = random.randint(1,maxSample)
               while newSiteNo in cue:
                  newSiteNo = random.randint(1,maxSample)
               if siteNo in redHerrings:
                  redHerrings.remove(siteNo)
                  redHerrings.append(newSiteNo)
               query = "SELECT URL FROM websiteList WHERE siteNo = '" + str(newSiteNo) +"'"
               result = connection.getOne(query)
               URL = result[0]
               # update the website information
               query = """UPDATE  websiteSamples SET URL = '"""+URL+ """'"""
               print("new website is: ",URL)
               connection.update(query)
               internalLinks = WebScraper.webScraper(connection,testID,URL,siteID)
         # set the site type and sample size
         if siteNo in redHerrings:
            print("RedHerring")
            query = """UPDATE websiteSamples SET type = 'redHerring' WHERE siteID = """+ str(siteID)
            connection.update(query)
         elif siteNo not in redHerrings:
            print("sample")
            query = """UPDATE websiteSamples SET type = 'sample' WHERE siteID = """+ str(siteID)
            connection.update(query)
            websiteDataCollection(connection,websiteSampleSize,internalLinks,siteID,testID) 
      Parser.Parser(connection,testID)
      connection.commit(connection)
      connection.close(connection)
      DataManipulation.dataManipulation(testID)
      Presentation.presentation(testID)
      controlFlag = 'false'


mainModule()




