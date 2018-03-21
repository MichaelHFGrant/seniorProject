#################################################################################
#   author:  Michael Grant                                                      #
#   Date:    Jan 2018                                                           #
#   Description:  SQL object which provides connection to the currrent database #
#                 , basic database queries and some specialized built in queries#
#################################################################################

import sqlite3, re

class sql():

   def __init__(self):

      self.connection = sqlite3.connect('database/csci491')
      self.getConfigQuery = """SELECT configID FROM tests WHERE testID ="""
      self.getSiteIDsQuery= """SELECT siteID FROM websiteSamples WHERE type = 'sample' and testID = """
      self.getPageIDsQuery= """SELECT siteID FROM websiteSamples \
               WHERE type = 'sample' AND testID = """
      self.insertWebpageSampleQuery = """INSERT INTO webpages (URL,pageID, rawData, siteID, pagetype) VALUES (:URL,:pageID, :rawData, :siteID, :Stype)"""

      
   def insertWebsiteSample(self,URL, pageID,rawData,siteID, Stype):
      self.connection.execute(self.insertWebpageSampleQuery,(URL,pageID,rawData,siteID,Stype))
      

   def query(self,query,arguments):
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
       result = self.connection.execute(self.getConfigQuery+str(testID))
       configID = result.fetchone()
       return configID[0]

   def getPageIDs(self,testID):
       pageIDs = []
       query = self.getPageIDsQuery+str(testID)
       result = self.connection.execute(query)
       siteIDs = result.fetchall()
       for siteID in siteIDs:
          query = """SELECT pageID FROM webpages WHERE siteID = """+str(siteID[0])
          result = self.connection.execute(query)
          pageIDs.extend(result.fetchall())
          pages = []
          for pageID in pageIDs:
              pages.append(pageID[0])
       return pages

   def getSiteIDs(self,testID):
       sites = []
       result = self.connection.execute(self.getSiteIDsQuery + str(testID))
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
    
   def commit(self):
      self.connection.commit()

   def close(self):
      self.connection.close()

   def printAll(self,testID):
      query = """select * from tests"""
      cur = self.connection.execute(query)
      print(cur.fetchall())
      query = """select * from methods"""
      print(cur.fetchall())

   def createTempTable(self,testID,traitList,method):
      print("This is createTempTable")
      siteStats ={}
      pageIDList = []
      connection.getOne("""DROP TABLE IF EXISTS """+method+"""Temp""")
      query = """CREATE TABLE IF NOT EXISTS """+method+"""Temp (pageID  INTEGER NOT NULL, siteID INTEGER NOT NULL)"""
      connection.getOne(query)
      siteIDs = connection.getSiteIDs(testID)
      print(traitList)
      for trait in traitList:
         # strip non alpha characters from traits
         column = re.search(r'[a-z]+',trait)
         query = """ALTER TABLE """+method+"""Temp ADD """+column.group()+""" INTEGER"""
         connection.getOne(query)
      for siteID in siteIDs:
         # get the stats for site
         siteStat = {}
         query = """SELECT mean,SD FROM sitestats WHERE siteID = """+str(siteID)+""" AND tagString = '"""
         for trait in traitList:
            innerQuery = query + trait+ """'"""
            siteStat[trait] = connection.getOne(innerQuery)
         siteStats[siteID[0]]=siteStat
         pageQuery = """SELECT pageID FROM webpages WHERE siteID = """+str(siteID)
         pageIDs = connection.getAll(pageQuery)
         for pageID in pageIDs:
            pageIDList.append(pageID)
            connection.getOne("""INSERT INTO """+method+"""Temp (pageID,siteID)VALUES ("""+str(pageID)+""","""+str(siteID)+""")""")
            # insert page data into temprary table for each trait in test
            for trait in traitList:
               query = """SELECT count FROM tagCount WHERE tagString = '"""+trait+"""' AND pageID ="""\
                                                                    +str(pageID)
               tagCount = connection.getOne(query)
               query = """SELECT sum(count) FROM tagCount WHERE pageID = """+str(pageID)
               total = connection.getOne(query)
               column = re.search(r'[a-z]+',trait)
               if tagCount and total and total[0]>0:
                  ratio = tagCount[0]/total[0]
                  query = """UPDATE """+method+"""Temp SET """+column.group()+"""= """+str(tagCount[0])+""" \
                                                          WHERE pageID ="""+str(pageID)
               else:
                  query = """UPDATE """+method+"""Temp SET """+column.group()+"""= 0  WHERE pageID ="""+str(pageID)
               connection.getOne(query)
      return (siteStats,pageIDList)


   def deleteTempTable(self,method):
      connection.getOne("""DROP TABLE IF EXISTS """+method+"""temp""")
