################################################################################
# Title:         Presentation
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   Produces the report of a system run
# Arguments:     testID
# Sub-processes: summery, body, conclusion,appendix,refrence
################################################################################

import GeneralProcesses


################################################################################
# Title:         summery
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   enters all relevant results and documentation for the report
#                summery
# Arguments:     database connection, testID
# Sub-processes: none
################################################################################

def summery(connection,testID):
   print("This is the summery process")


################################################################################
# Title:         body
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   enters relevant results and documentation for the report body
# Arguments:     database connection, testID 
# Sub-processes: none
################################################################################

def body(connection,testID):
   print("This is the body process")


################################################################################
# Title:         conclusion
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   enters relevant results and documentation for the report
#                conclusion
# Arguments:     database connection, testID
# Sub-processes: none
################################################################################

def conclusion(connection,testID):
   print("This is the conclusion process")


################################################################################
# Title:         appendix
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   enters relevant reslts and documentation needed to the appendix
# Arguments:     database connection, testID
# Sub-processes: none
################################################################################

def appendix(connection,testID):
   print("This is the appendix process")



################################################################################
# Title:         reference
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   produces a properly formatted refernece list of sources used
#                in the report
# Arguments:     database connection, testID
# Sub-processes: none
################################################################################

def reference(connection,testID):
   print("This is the reference process")

def presentation(testID):
   connection = GeneralProcesses.sql()
   print("This is the Presentation Module")
   # get the methods which were involved in the test
   query = """SELECT name FROM methods WHERE testID = """+str(testID)
   methods = connection.getAll(query)
   pageIDs = connection.getPageIDs(testID)
   siteIDs = connection.getSiteIDs(testID)
   
   for method in methods:
      if method[0] == 'RarePairs':
         print("Results for RarePairs method of stylometic analysis")
         print("siteID   accuracy")
         query = """SELECT siteID, accuracy FROM results WHERE testID = """+ str(testID)
         results = connection.getAll(query)
         for result in results:
            siteID, score = result
            print(siteID,'      ',score)
            
      if method[0] == 'WriterInvariant':
         print('Results for WriterInvariant method of sylometric analysis')
         print('siteID   accuracy')
         query = """SELECT siteID, tagList, accuracy FROM tagLists WHERE testID = """+str(testID)
         results = connection.getAll(query)
         for result in results:
            print(result[0],'   ',result[1],'   ',result[2])
            
      if method[0] == 'GeneticAlgorithm':
         query = """SELECT siteID, accuracy, solution FROM signatures \
                    WHERE testID = """+str(testID)
         results = connection.getAll(query)
         
         print("Results for GeneticAlgorithm method of stylometic analysis")
         print("siteID   accuracy   solution")
         for result in results:
            print(result[0],'      ',result[1],'   ',result[2])
            
      if method[0] == 'NeuralNetwork':
         print("Results for NeuralNetwork method of stylometic analysis")
         print("siteID   error")
         query = """SELECT error FROM networkResults WHERE siteID = """
         for siteID in siteIDs:
            innerQuery = query+ str(siteID)
            error = connection.getOne(innerQuery)
            print(siteID,'      ',error[0])
            
   summery("connection","testID")
   body("connection","testID")
   conclusion("connection","testID")
   appendix("connection","testID")
   reference("connection","testID")


#presentation(17)
