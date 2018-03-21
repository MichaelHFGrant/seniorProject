
# Parser Module
import GeneralProcesses, subprocess, re

def tagCount(connection,pageIDs,traits):
   print('This is tagCount process')
   for pageID in pageIDs:
      query = "SELECT tag FROM tags where pageID ="+ str(pageID[0])
      tagDict = {}
      for tag in connection.getAll(query):
         Tag = re.search(r'<[a-z]+',tag[0])
         if Tag:
            if Tag.group() in tagDict:
               tagDict[Tag.group()]+=1
            else:
               tagDict[Tag.group()] = 1
      for tag in tagDict:
         query = "INSERT INTO tagcount(pageID,tagString,count) VALUES(:pgID,:tag,:count)"
         connection.query(query,(pageID[0],tag,tagDict[tag]))


    
def Parser(connection,testID):
   print("This is the Parser Module")
   traitList = {}
   pageIDs = []
   # get a list of webpages in the current test
   query = """SELECT siteID FROM websiteSamples WHERE testID ="""+str(testID)
   siteIDs = connection.getAll(query)
   for siteID in siteIDs:
       query = """SELECT pageID FROM webpages WHERE siteID = :siteID"""
       pages = connection.query(query,siteID)
       for page in pages:
           pageIDs.append(page)
   # get all methods requested for test
   query = """SELECT name FROM methods WHERE testID = """+str(testID)
 
   # get all the traits in the test
   methods = connection.getAll(query)
   print(methods)
   for method in methods:
       query = """SELECT DISTINCT T.traitID,Ngram, T.RExp,T.testCode  FROM traits T, traitList L\
                                                    WHERE T.traitID = L.traitID\
                                                    AND L.method = '"""+ method[0]+"""'"""
       methodTraits = connection.getAll(query)
       for trait in methodTraits:
           for page in pageIDs:
              pageID = str(page[0])
              query = """select tag from tags where pageID ="""+str(pageID)
              tags = connection.getAll(query)
              # for each trait in the list apply the correct code
              N = trait[1]
              RExp = trait[2]
              traitCode = trait[3]
              traitCodetest = """
"""
              # call the traitCode for each page
              code = compile(traitCode,"string","exec")
              exec(code)


#connection = GeneralProcesses.sql()
#Parser(connection,3)
#connection.commit(connection)
