################################################################################
# Title:         WriterInvariant 
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   Module which provides the stylometic method of the Writer Invariant
# Arguments:     testID
# Sub-processes: binning
################################################################################

import GeneralProcesses

################################################################################
# Title:          binning
# Author:         Michael Grant
# Date:           Sept 2017
# Description:    process for building a trait tree from sample data
# Arguments:      testID
# Sub-processes:  None
################################################################################

def binning(tag,mean,SD,pageStats):
    print("This is the binning process")
    binnedPages = []
    unbinnedPages = []
    pageIDs = pageStats.keys()
    for page in pageIDs:
        count = None
        for item in pageStats[page]:
            if item[0] == tag:
                count = item[1]
        if count:
            if abs(mean-count)<= SD:
                binnedPages.append(page)
            else:
                unbinnedPages.append(page)
        else:
            unbinnedPages.append(page)
    return (binnedPages,unbinnedPages)

################################################################################
# Title:          modelTraining
# Author:         Michael Grant
# Date:           Oct 2017
# Description:    build a model for identifying each of the websites
# Arguments:      siteStats, pageStats,testList,tagList
# Sub-processes:  Binning Process
################################################################################

def modelTraining(connection,testID,siteStats,pages,testList,tagLists):
    print("This is the modelTraining process")
    topRank = 0
    siteCount=0
    binCount=0
    # top stopping conditions
    if len(testList)<=0:
        return tagLists
    # if only pages from one site are passed to modeltraining
    if len(siteStats.keys())<2:
           return tagLists
    bestTag = testList[0]
    for test in testList:
        for siteID in siteStats.keys():
            keyData = siteStats[siteID]
            if test[0] in keyData.keys():
                (mean,SD) = keyData[test[0]]
            else:
                mean,SD = 0,0
            (binned,unbinned) = binning(test[0],mean,SD,pages)
            print(binned,' ',unbinned)
             # rank the solutions
            rank = GeneralProcesses.ranking(connection,testID,siteStats,binned,unbinned)
            if rank >= topRank:
                topRank = rank
                bestTag = test
                bestRange = (mean,SD)
    (binned,unbinned)=binning(bestTag[0],bestRange[0],bestRange[1],pages)
    testList.remove(bestTag)
    print(testList)
    binnedSites = {}
    unbinnedSites={}
    binnedPages= {}
    unbinnedPages = {}
    for siteID in siteStats.keys():
        query = """SELECT pageID FROM webpages WHERE pageType = 'sample' AND siteID = """+str(siteID)
        sitePages = connection.getAll(query)
        binCount=0
        for page in sitePages:
            if page[0] in binned:
                binCount+=1
        if len(sitePages)>0:
            if binCount/len(sitePages) >= .4:
                for page in sitePages:
                    binnedPages[page[0]] = pages[page[0]]
                binnedSites[siteID] = siteStats[siteID]
                tagLists[siteID].append(bestTag)
            else:
                for page in sitePages:
                    unbinnedPages[page[0]] = pages[page[0]]
                unbinnedSites[siteID] = siteStats[siteID]
    if len(binned)>0:
        tagLists = modelTraining(connection,testID,binnedSites,binnedPages,testList,tagLists)
    if len(unbinned)>0:
        tagLists = modelTraining(connection,testID,unbinnedSites,unbinnedPages,testList,tagLists)
    return tagLists

################################################################################
# Title:          testModel
# Author:         Michael Grant
# Date:           Sept 2017
# Description:    implements the Writer Invaraint stylometric method
# Arguments:      testID
# Sub-processes:  None
################################################################################

def testModel(connection,testID,siteStats,tagLists):
    print("This is the testModel Processs")
    pageIDs =[]
    query = """SELECT pageID FROM webpages WHERE pageType = 'test' AND siteID = """
    for siteID in siteStats.keys():
        pageIDs.extend(connection.getAll(query+str(siteID)))
    print(pageIDs)
    pageStats = {}
    # get the pageData needed for testing the solution
    query = """SELECT count(*) FROM tagCount WHERE tagString = :tagName AND pageID = :pageID"""
    for pageID in pageIDs:
        pageStat = []
        for tag in tagLists:
            pageStat.append((tag,connection.query(query,(tag,pageID[0]))))
        pageStats[pageID]=pageStat
    for siteID in siteStats.keys():
        print(siteID,' ',siteStats[siteID])
        for tag in tagLists[siteID]:
           tagString = ':'.join(tag)
           Stats = siteStats[siteID]
           for siteID in siteStats.keys():
               (mean,SD) = Stats[tag[0]]
               #bin the pages using the siteData and the tags in the taglist
               (binned,unbinned) = binning(tag[0],mean,SD,pageStats)
               rank = GeneralProcesses.ranking(connection,testID,siteStats,binned,unbinned)
               query = """INSERT INTO tagLists(testID,siteID,tagList,accuracy) VALUES (:testID,:siteID,:tagList,:rank)"""
           connection.query(query,(testID,siteID,tagString,rank))
    return(1,2)
    
    
################################################################################
# Title:          writerInvariant
# Author:         Michael Grant
# Date:           Sept 2017
# Description:    implements the Writer Invaraint stylometric method
# Arguments:      testID
# Sub-processes:  None
################################################################################


def writerInvariant(connection,testID):

    
   print("This is the writerInvariant process")
   (siteStats,pageStats) = GeneralProcesses.getStats(connection,testID,"WriterInvariant","sample")
   siteIDs = siteStats.keys()
   pageIDs = pageStats.keys()
   testData={}
   tagLists = {}
   query = """SELECT args FROM traitList WHERE configID = (SELECT configID from tests where testID = """+str(testID)+""") AND method = 'WriterInvariant'"""
   testList = connection.getAll(query)
   print(testList)
   for siteID in siteIDs:
       tagLists[siteID]=[]
       siteData={}
       datum = siteStats[siteID]
       for data in datum:
           if not data:
               continue
           (tag,mean,SD) = data[0]
           siteData[tag] = (mean,SD)
       testData[siteID] = siteData
   tagLists = modelTraining(connection,testID,testData,pageStats,testList,tagLists)
   # test the accuracy of the model
   (TP,TN) = testModel(connection,testID,testData,tagLists)
   for tagList in tagLists:
       print(tagList,' ',tagLists[tagList])
 #  return "success"


   
#connection = GeneralProcesses.sql()
#writerInvariant(connection,13)
