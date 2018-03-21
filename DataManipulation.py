################################################################################
# Title:         DataManipulation
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   Preforms the stylometric analysis needed by the system
# Arguments:     testID, 
# Sub-processes: statisticalAnlysis, getStats, binning, rarePairs, writerInvariant
#                geneticAlgorithms, neuralNetworks
################################################################################


import WriterInvariant, RarePairs, GeneticAlgorithm, NeuralNetwork, GeneralProcesses,subprocess,math,random

# DataManipulation  Module
################################################################################
# Title:         statisticalAnalysis
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   Analyzes the parsed meta-data using the requested statistical
#                methods
# Arguments:     testID, statTest
# Sub-processes: None
################################################################################

def statisticalAnalysis(connection,testID,siteID,test,argument,condition= None):
   print("This is the statisticalAnalysis process")

   tagList = []
   siteData = []
   tagList = []
   query = """SELECT pageID FROM webpages WHERE siteID = """+str(siteID[0])
   pageIDs = connection.getAll(query)
   for pageID in pageIDs:
      tagQuery = """SELECT tagString, count FROM """+test+"""  WHERE pageID = """+str(pageID[0])
      if condition:
         tagQuery+= condition
      tagDatum = connection.getAll(tagQuery)
      pageData = {}
      for tagData in tagDatum:
         (tag,count) = tagData
         pageData[tag] = count
         if tag not in tagList:
            tagList.append(tag)
      siteData.append(pageData)
   siteStats = calculateStats(siteData,tagList)
   siteQuery = """INSERT INTO siteStats(siteID,method,tagString,mean,SD)\
                                    VALUES(:siteID,:test,:tag,:mean,:SD)"""
   for stat in siteStats:
      (mean,SD) = siteStats[stat]
      connection.query(siteQuery,(siteID[0],test,stat,mean,SD))
      connection.commit(connection)

def calculateStats(siteData,tagList):
   stats = {}
   for tag in tagList:
      total = 0
      values = []
      for page in siteData:
         if tag in page:
            values.append(page[tag])
            total = total + page[tag]
      # calculate the mean and standard deviation of each tags for the site
      mean = total/len(siteData)
      x = 0
      for value in values:
         newVal = float(value)
         x = x+ (newVal - mean)*(newVal-mean)
      if len(siteData)>1:
         SD = math.sqrt(x/(len(siteData)-1))
      else:
         SD = 0
      stats[tag] = (mean,SD)
   return stats


      

################################################################################
# Title:         getStats 
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   Accesses the database and retrieves all the statistical data
#                needed to perform stylometric analysis
# Arguments:     testID
# Sub-processes: None
################################################################################

def getStats(connection,testID,method):
   print("This is the getStats process")
   siteData = {}
   pages ={}
   query ="""SELECT siteID from websiteSamples where testID = """+ str(testID)
   siteIDs = connection.getAll(query)
   query = """ SELECT DISTINCT statTest FROM traitList WHERE method = '"""+method+"""'"""
   tests = connection.getAll(query)
   for test in tests:
      for siteID in siteIDs:
         query = """SELECT tag, mean, SD FROM siteStats WHERE siteID = """+str(siteID[0])+\
                                                      """ AND method = '"""+test[0]+"""'"""
         siteData[siteID[0]]=connection.getAll(query)
         query = """SELECT pageID FROM webpages WHERE siteID = """+ str(siteID[0])
         pageIDs = connection.getAll(query)
         for pageID in pageIDs:
            query = """SELECT tagString, count FROM """+test[0]+""" WHERE pageID = """+str(pageID[0])
            pageData = connection.getAll(query)
            pages[pageID[0]] = pageData
   return (siteData,pages)
         


################################################################################
# Title: 
# Author:  Michael Grant
# Date:
# Description:
# Arguments:
# Sub-processes:
################################################################################

def dataManipulation(testID):
   print("This is the DataManipulation Module")
   # system init
   connection = GeneralProcesses.sql()
   query = """SELECT name FROM methods WHERE testID = """+str(testID)
   methods = connection.getAll(query)
   query = """SELECT siteID FROM websiteSamples WHERE testID = """+str(testID)
   siteIDs = connection.getAll(query)
   for siteID in siteIDs:
   # choose testPage for each site
      pageIDs=connection.getAll("""SELECT pageID FROM webpages WHERE siteID = """+str(siteID[0]))
      for pageID in pageIDs:
         connection.getOne("""UPDATE webpages SET pageType = 'sample' WHERE pageID = """+str(pageID[0]))
      if len(pageIDs)>1:
         testPage = random.randint(0,len(pageIDs)-1)
         pageID=pageIDs[testPage]
         connection.getOne("""UPDATE webpages SET pageType = 'test' WHERE pageID = """+str(pageID[0]))
      if len(pageIDs) == 1:
         connection.getOne("""UPDATE webpages SET pageType = 'test' WHERE pageID = """+str(pageID[0]))
   query = """SELECT DISTINCT statTest, args,condition FROM traitList WHERE method = '"""
   for method in methods:
      innerQuery = query + method[0] + """'"""
      results = connection.getAll(innerQuery)
      for result in results:
         (test,argument,condition) = result
         for siteID in siteIDs:
            #call stat analysis process
            statisticalAnalysis(connection,testID,siteID,test,argument,condition)
      # perform the stylometric analysis for current method
      if method[0] == 'RarePairs':
         RarePairs.rarePairs(connection,testID)
      if method[0] == 'WriterInvariant':
         WriterInvariant.writerInvariant(connection,testID)
      if method[0] == 'GeneticAlgorithm':
         GeneticAlgorithm.geneticAlgorithm(connection,testID)
      if method[0] == 'NeuralNetwork':
         NeuralNetwork.neuralNetwork(connection,testID)
   connection.commit(connection)

#dataManipulation(7)



