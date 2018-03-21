# General Processes


import sqlite3, re

def timer(function,arguments,time=0):
   if (time == 0):
      time = random.randint(5,30)
   sleep(time)
   result = function(*arguments)
   
   print("This is the Timer Process")

class sql():

   def __init__(self):

      self.connection = sqlite3.connect('database/csci491')

      
   def insertWebsiteSample(self, pageID,rawData,siteID):
      query = self.insertWebsiteQuery
      curser = self.connection.execute(query,(pageID,rawData,siteID,Stype))
      

   def query(self,query,arguments):
      query = query
      curser = self.connection.execute(query,arguments)
      result = curser.fetchall()
      return result

   def getOne(self,query):
      curser  = self.connection.execute(query)
      result = curser.fetchone()
      return result

   def getAll(self,query):

      curser = self.connection.execute(query)
      result = curser.fetchall()
      return result


   def insert(self,table,arguments,argumentNames):
      temp = []
      for argument in arguments:
         if (type(argument) == int):
            temp.insert(len(temp)+1,str(argument))
         else:
            temp.insert(len(temp)+1,argument)
            
      tempValues ="','".join(temp)
      values = "'"+tempValues+"'"
      columns = ','.join(argumentNames)
      query = "INSERT INTO " + table + "("+columns+") VALUES("+values+")"
      curser = self.connection.execute(query)
      return curser
   
   def update(self,query):
      curser = self.connection.execute(query)
      return curser

   def getID(self,tableName):
      query = "SELECT count(*) FROM " + tableName
      curser = self.connection.execute(query)
      result = curser.fetchone()
      return result[0]+1

   def getConfig(self,testID):
       result = self.connection.execute("""SELECT configID FROM tests WHERE testID = """+str(testID))
       configID = result.fetchone()
       return configID[0]

   def getPageIDs(self,testID):
       pageIDs = []
       query = """SELECT siteID FROM websiteSamples \
               WHERE type = 'sample' AND testID = """+str(testID)
       result = self.connection.execute(query)
       siteIDs = result.fetchall()
       for siteID in siteIDs:
          query = """SELECT pageID FROM webpages WHERE siteID = """+str(siteID[0])
          result = self.connection.execute(query)
          pageIDs.extend(result.fetchall())
       return pageIDs

   def getSiteIDs(self,testID):
       sites = []
       query = """SELECT siteID FROM websiteSamples \
               WHERE type = 'sample' AND testID = """+str(testID)
       result = self.connection.execute(query)
       siteIDs = result.fetchall()
       for siteID in siteIDs:
          sites.append(siteID[0])
       return sites

   def getData(self,trait,pageID,method):
      tag = re.search(r'[a-z]+',trait)
      query = """SELECT """+tag.group()+""" FROM """+method+"""temp WHERE pageID = """+str(pageID)
      result = self.connection.execute(query)
      data = result.fetchone()
      return data[0]
    
   def commit(self,connection):
      self.connection.commit()

   def close(self,connection):
      self.connection.close()

   def printAll(self,testID):
      query = """select * from tests"""
      cur = self.connection.execute(query)
      print(cur.fetchall())
      query = """select * from methods"""
      print(cur.fetchall())


################################################################################
# Title:         getStats 
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   Accesses the database and retrieves all the statistical data
#                needed to perform stylometric analysis
# Arguments:     testID
# Sub-processes: None
################################################################################

def getStats(connection,testID,method,dataType):
   siteData = {}
   pages ={}
   print("This is the getStats process")
   query ="""SELECT siteID  from websiteSamples where testID = """+ str(testID) + """ \
                                                       AND type = '"""+ 'sample'+"""'"""
   siteIDs = connection.getAll(query)
   query = """ SELECT  statTest,args,condition FROM traitList WHERE method = '"""+method+"""'"""
   tests = connection.getAll(query)
   for siteID in siteIDs:
      siteData[siteID[0]]=[]
      for test in tests:
         (statTest,arg,condition) = test
         query = """SELECT tagString,mean,SD FROM siteStats WHERE siteID = """ + str(siteID[0])+\
                                                      """ AND method = '""" + statTest+"""'"""
         if condition:
            query += condition
         siteData[siteID[0]].append(connection.getAll(query))
      query = """SELECT pageID FROM webpages WHERE pageType = 'sample' AND siteID = """+ str(siteID[0])
      pageIDs = connection.getAll(query)
      for pageID in pageIDs:
         query = """SELECT tagString, count FROM """+test[0]+""" WHERE pageID = """+str(pageID[0])
         pageData = connection.getAll(query)
         pages[pageID[0]] = pageData
   return (siteData,pages)



def getTestingStats(connection,testID,method):
   siteData = {}
   pages ={}
   print("This is the getStats process")
   query ="""SELECT siteID  from websiteSamples where testID = """+ str(testID) + """ \
                                                       AND type = '"""+ 'sample'+"""'"""
   siteIDs = connection.getAll(query)
   query = """ SELECT  statTest,args,condition FROM traitList WHERE method = '"""+method+"""'"""
   tests = connection.getAll(query)
   for siteID in siteIDs:
      siteData[siteID[0]]=[]
      for test in tests:
         (statTest,arg,condition) = test
         query = """SELECT tagString,mean,SD FROM siteStats WHERE siteID = """ + str(siteID[0])+\
                                                      """ AND method = '""" + statTest+"""'"""
         if condition:
            query += condition
         siteData[siteID[0]].append(connection.getAll(query))
      query = """SELECT pageID FROM webpages WHERE pageType = 'test' AND siteID = """+ str(siteID[0])
      pageIDs = connection.getAll(query)
      for pageID in pageIDs:
         query = """SELECT tagString, count FROM """+test[0]+""" WHERE pageID = """+str(pageID[0])
         pageData = connection.getAll(query)
         pages[pageID[0]] = pageData
   return (siteData,pages)





################################################################################
# Title:         accuacy 
# Author:        Michael Grant
# Date:          Oct 2017
# Description:   calculaes the accuracy of a given test
#                needed to perform stylometric analysis
# Arguments:     testID
# Sub-processes: None
################################################################################


def accuracy(connection,testID,siteID):
   print("This is the accuracy process")
   query = """SELECT pageID, result FROM pageResults WHERE siteID = """+str(siteID)
   results = connection.getAll(query)
   TP,TN,FP,FN = (0,0,0,0)
   for result in results:
      pageID,score = result
      query = """select siteID from webpages where pageID = """+str(pageID)
      correctSite = connection.getOne(query)
         
      if score > .8 and correctSite[0] == siteID:
         TP +=1
      elif score >.8 and correctSite[0] != siteID:
         FP +=1
      elif score <.8 and correctSite[0] == siteID:
         FN +=1
      elif score <.8 and correctSite[0] != siteID:
         TN +=1
   if result:
      acc = (TP+TN)/(TP+TN+FP+FN)
   return acc

################################################################################
# Title:         ranking 
# Author:        Michael Grant
# Date:          Oct 2017
# Description:   determines the rank of a solution 
#                needed to perform stylometric analysis
# Arguments:     
# Sub-processes: None
################################################################################

def ranking(connection,testID,siteStats,binned,unbinned):
   print("This is The Ranking Process")
   query = """SELECT webpageSampleSize FROM samples WHERE configID =\
                              (SELECT configID FROM tests where testID = """+str(testID)+""")"""
   sampleSize = connection.getOne(query)
   query = """SELECT pageID from webpages WHERE siteID = """
   
   binCount =0
   unbinCount = 0
   binnedSites=[]
   unbinnedSites = []
   for siteID in siteStats.keys():
      innerQuery = query+str(siteID)
      pageIDs = connection.getAll(innerQuery)
      for pageID in pageIDs:
         if pageID[0] in binned:
             if siteID not in binnedSites:
               binnedSites.append(siteID)
         else:
             if siteID not in unbinnedSites:
               unbinnedSites.append(siteID)      
   if len(binnedSites)<1:
      return 0
   if len(unbinnedSites) <1:
      return 0
   binCount = len(binned)
   unbinCount = len(unbinned)
   rank = binCount/(len(binnedSites)*sampleSize[0]) + unbinCount/(len(unbinnedSites)*sampleSize[0])
   return rank


def getSamplePages(connection,testID):
   # get the siteIDs used in test
   query = """SELECT siteID FROM websiteSamples WHERE type = 'sample' AND testID = """+str(testID)
   print(query)
   siteIDs = connection.getAll(query)
   print(siteIDs)




def createTempTable(connection,testID,traitList,method):
   print("This is createTempTable")
   siteStats ={}
   pageIDList = []
   connection.getOne("""DROP TABLE IF EXISTS """+method+"""Temp""")
   query = """CREATE TABLE IF NOT EXISTS """+method+"""Temp (pageID  INTEGER NOT NULL, siteID INTEGER NOT NULL)"""
   connection.getOne(query)
   query = """SELECT siteID FROM websiteSamples WHERE testID = """+str(testID)
   siteIDs = connection.getAll(query)
   print(traitList)
   for trait in traitList:
      # strip non alpha characters from traits
      column = re.search(r'[a-z]+',trait)
      query = """ALTER TABLE """+method+"""Temp ADD """+column.group()+""" INTEGER"""
      connection.getOne(query)
   for siteID in siteIDs:
      # get the stats for site
      siteStat = {}
      query = """SELECT mean,SD FROM sitestats WHERE siteID = """+str(siteID[0])+""" AND tagString = '"""
      for trait in traitList:
         innerQuery = query + trait+ """'"""
         siteStat[trait] = connection.getOne(innerQuery)
      siteStats[siteID[0]]=siteStat
      pageQuery = """SELECT pageID FROM webpages WHERE siteID = """+str(siteID[0])
      pageIDs = connection.getAll(pageQuery)
      for pageID in pageIDs:
         pageIDList.append(pageID[0])
         connection.getOne("""INSERT INTO """+method+"""Temp (pageID,siteID)VALUES ("""+str(pageID[0])+""","""+str(siteID[0])+""")""")
         # insert page data into temprary table for each trait in test
         for trait in traitList:
            query = """SELECT count FROM tagCount WHERE tagString = '"""+trait+"""' AND pageID ="""\
                                                                    +str(pageID[0])
            tagCount = connection.getOne(query)
            query = """SELECT sum(count) FROM tagCount WHERE pageID = """+str(pageID[0])
            total = connection.getOne(query)
            column = re.search(r'[a-z]+',trait)
            if tagCount and total and total[0]>0:
               ratio = tagCount[0]/total[0]
               query = """UPDATE """+method+"""Temp SET """+column.group()+"""= """+str(tagCount[0])+""" \
                                                          WHERE pageID ="""+str(pageID[0])
            else:
               query = """UPDATE """+method+"""Temp SET """+column.group()+"""= 0  WHERE pageID ="""+str(pageID[0])
            connection.getOne(query)
   return (siteStats,pageIDList)


def deleteTempTable(connection,method):
   connection.getOne("""DROP TABLE IF EXISTS """+method+"""temp""")
