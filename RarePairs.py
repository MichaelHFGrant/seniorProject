################################################################################
# Title:         RarePairs 
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   Implements the rare pairs method of stymometric analysis
# Arguments:     testID, webpage statistics
# Sub-processes: TO BE DETERMINED
################################################################################

import GeneralProcesses,random



def rarePairs(connection,testID):
   print("This is the rarePairs process")
   # get the test data
   (siteData,pageStats) = GeneralProcesses.getStats(connection,testID,"RarePairs","sample")
   siteIDs = siteData.keys()
   pageIDs = pageStats.keys()
   results = {}
   for siteID in siteIDs:
      siteStats = {}
      for datum in siteData[siteID]:
         for tag in datum:
            (tag,mean,SD) = tag
            siteStats[tag] = (mean,SD)
      for pageID in pageIDs:
         memCount = 0
         for tagData in pageStats[pageID]:
            (tagString,count) =tagData
            if tagString in siteStats.keys():
               (mean,SD) = siteStats[tagString]
               memCount += .6
               if abs(count-mean) <= SD:
                  memCount +=.4
         if len(pageStats[pageID])>0:
            result = memCount/len(pageStats[pageID])
         else:
            result = 0
         query = """INSERT INTO pageResults (siteID,pageID,result) VALUES(:siteID,:pageID,:result)"""
         connection.query(query,(siteID,pageID,result))
         
      acc=GeneralProcesses.accuracy(connection,testID,siteID)
      query = """INSERT INTO results (testID,siteID,accuracy) VALUES(:testID,:siteID,:Accuracy)"""
      connection.query(query,(testID,siteID,acc))
   return "success"


#connection = GeneralProcesses.sql()
#rarePairs(connection,10)
#connection.commit(connection)
