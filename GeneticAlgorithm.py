################################################################################
# Title:         GeneticAlgorithm
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   Implements the genetic algorithm method of stylometric analysis
# Arguments:     testID, webpage statistics
# Sub-processes: randomSolutions, fitnessTest, combining, ranking, mutation
################################################################################

import GeneralProcesses, random, re



################################################################################
# Title:         fitness 
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   applies the fitness test to given solution and returns a value
#                representing the solutions fitness score
# Arguments:     fitness test, solution
# Sub-processes: None
################################################################################


def fitnessProcess(connection,solutions,fitness,siteID,pageIDs):
   
   print("This is fitness")
   ranks = {}
   solutionCount = 0
   for solution in solutions:
      solutionCount +=1
      positive = []
      negative = []
      
      for pageID in pageIDs:
         count = 0
         for trait in solution.keys():
            tag =re.search(r'[a-z]+',trait)
            (minCount,MaxCount)= solution[trait]
            if tag.group() == 'table':
               
               query="""SELECT atable FROM GeneticTemp WHERE pageID = """+str(pageID)
            else:
               query="""SELECT """+tag.group()+""" FROM GeneticTemp WHERE pageID = """+str(pageID)
            tagCount = connection.getOne(query)
            if tagCount:
               if float(tagCount[0]) <=MaxCount and float(tagCount[0])>= minCount:
                  count +=1
         if count/len(solution.keys()) > int(fitness):
            positive.append(pageID)
         else:
            negative.append(pageID)
      rank = calculateRank(connection,siteID,positive,negative)

      ranks[solutionCount]= (rank,solution)
   return(ranks)

################################################################################
# Title:         ranking 
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   ranks all solutions from most fit to least fit
# Arguments:     solutions
# Sub-processes: none
################################################################################


def calculateRank(connection,siteID,positive,negative):
   # get the pages which bto current siteID
   query = """SELECT pageID FROM webpages WHERE siteID = """+str(siteID)
   TP = 0
   FN = 0
   pageIDs = connection.getAll(query)
   for pageID in pageIDs:
      if pageID[0] in positive:
         TP +=1
      else:
         FN +=1
   FP = len(positive)-TP
   TN = len(negative)-FN
   rank = (TP+TN)/(len(positive)+len(negative))
   return rank
            

   

################################################################################
# Title:         ranking 
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   ranks all solutions from most fit to least fit
# Arguments:     solutions
# Sub-processes: none
################################################################################

def rankingProcess(solutionsFitnesses):
   print("This is ranking")
   newSolutions = []
   
   for y in range(1,len(solutionsFitnesses.keys())):
      for z in range(y,len(solutionsFitnesses.keys())-1):
         if solutionsFitnesses[y][0] < solutionsFitnesses[z][0]:
            temp = solutionsFitnesses[y]
            solutionsFitnesses[y]=solutionsFitnesses[z]
            solutionsFitnesses[z] = temp
   topSolutions = int(len(solutionsFitnesses.keys())/2)
   for y in range(1,topSolutions+1):
      newSolutions.append(solutionsFitnesses[y][1])
   return newSolutions

         
      
      
   
   
   
################################################################################
# Title:         randomSolutionGen 
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   produces the given number of random solutions requested
# Arguments:     number of solutions, number of traits per solution
# Sub-processes: None
################################################################################

def randomSolutionGen(solutionCount,traitLists):
   print("This is the randomSolutionGen")
   random.seed()
   solutions = []
   # get the maximum and minimum count for each trait in the test
   for count in range(solutionCount):
      solution = {}
      for trait in traitLists.keys():
         (minCount,maxCount) = traitLists[trait]
         if maxCount:
            lower = random.uniform(minCount,maxCount)
            upper = random.uniform(lower,maxCount)
            solution[trait]=(lower,upper)
      solutions.append(solution)
   return solutions


################################################################################
# Title:         combination 
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   combines the given solutions together to produce double the
#                solutions given
# Arguments:     solutons, combining rule
# Sub-processes:
################################################################################
def combinationProcess(solutions,siteStats):
   print("This is combination")
   newSolutions = []
   for solution in range(0,len(solutions)):
      mate = solution
      while mate == solution:
         mate =random.randint(0,len(solutions)-1)
      newSolution = {}
      for trait in solutions[solution].keys():
         (firstLow,firstHigh)=solutions[solution][trait]
         (secondLow,secondHigh)=solutions[mate][trait]
         newSolution[trait] = (firstLow-(firstLow-secondLow)*.4,firstHigh-(firstHigh-secondHigh)*.4)
      newSolutions.append(newSolution)
   for newSolution in newSolutions:
      solutions.append(newSolution)

################################################################################
# Title:         mutation 
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   randomly changes the given solution 
# Arguments:     solution
# Sub-processes: none
################################################################################

def mutationProcess(solutions):
   print("This is mutation")
   random.seed()
   solution = random.randint(0,len(solutions)-1)
   mutate = random.randint(0,3)
   traitNumber = len(solutions[solution].keys())
   count = random.randint(0,traitNumber)
   for key in solutions[solution]:
      if count == 0:
         (Low,High)=solutions[solution][key]
         if mutate == 0:
            solutions[solution][key] = (max(0,Low-(High-Low)*.3),High-(High-Low)*.3)
         if mutate == 1:
            solutions[solution][key] = (max(0,Low+(High-Low)*.3),High+(High-Low)*.3)
         if mutate == 2:
            solutions[solution][key] = (max(0,Low-(High-Low)*.3),High+(High-Low)*.3)
         if mutate == 3:
            solutions[solution][key] = (max(0,Low+(High-Low)*.3),High-(High-Low)*.3)
      count-=1


   
   
################################################################################
# Title:         createTempTable
# Author:        Michael Grant
# Date:          nov 2017
# Description:   Porcess for implementing a genetic algorithm
# Arguments:     connection,traitList
# Sub-processes: none
################################################################################

def createTempTable(connection,traitList,siteIDs,solutions):
   print("This is createTempTable")
   siteStats ={}
   pageIDList = []
   connection.getOne("""DROP TABLE IF EXISTS geneticTemp""")
   query = """CREATE TABLE IF NOT EXISTS GeneticTemp (pageID  INTEGER NOT NULL)"""
   connection.getOne(query)
   
   
   for trait in traitList:
      
      # strip non alpha characters from traits
      column = re.search(r'[a-z]+',trait[0])
      if column.group() == 'table':
         query = """ALTER TABLE GeneticTemp ADD """+'aTable'+""" INTEGER"""
      else:
         query = """ALTER TABLE GeneticTemp ADD """+column.group()+""" INTEGER"""
      connection.getOne(query)

   for siteID in siteIDs:
      # get the stats for site
      siteStat = {}
      query = """SELECT mean,SD FROM sitestats WHERE siteID = """+str(siteID[0])+""" AND tagString = '"""
      for trait in solutions[0].keys():
         innerQuery = query + trait+ """'"""
         siteStat[trait] = connection.getOne(innerQuery)
      siteStats[siteID[0]]=siteStat
      pageQuery = """SELECT pageID FROM webpages WHERE siteID = """+str(siteID[0])
      pageIDs = connection.getAll(pageQuery)
      for pageID in pageIDs:
         pageIDList.append(pageID[0])
         connection.getOne("""INSERT INTO GeneticTemp (pageID)VALUES ("""+str(pageID[0])+""")""")
         # insert page data into temprary table for each trait in test
         for trait in traitList:
            query = """SELECT count FROM tagCount WHERE tagString = '"""+trait[0]+"""' AND pageID ="""\
                                                                    +str(pageID[0])
            tagCount = connection.getOne(query)
            column = re.search(r'[a-z]+',trait[0])
            if tagCount:
               if column.group() == 'table':
                  query = """UPDATE GeneticTemp SET """+'aTable'+"""= """+str(tagCount[0])+""" \
                                                          WHERE pageID ="""+str(pageID[0])
               else:
                   query = """UPDATE GeneticTemp SET '"""+column.group()+"""'= """+str(tagCount[0])+""" \
                                                          WHERE pageID ="""+str(pageID[0])
            else:
               if column.group() == 'table':
                  query = """UPDATE GeneticTemp SET """+'aTable'+"""= 0 WHERE pageID ="""+str(pageID[0])
               else:
                  query = """UPDATE GeneticTemp SET '"""+column.group()+"""'= 0  WHERE pageID ="""+str(pageID[0])
            connection.getOne(query)
   return (siteStats,pageIDList)
################################################################################
# Title:         solutionTest
# Author:        Michael Grant
# Date:          Nov. 2017
# Description:   test the solutions for accuracy on test pages
# Arguments:     connection, testID 
# Sub-processes: randomSolutionGen, fitness, ranking, combination, mutation
################################################################################

def testSolution(connection,solution,fitness,siteID,testPageList):
   print("This is testSolution")
   positive =[]
   negative =[]
   for pageID in testPageList:
      count = 0
      for trait in solution:
         tag =re.search(r'[a-z]+',trait)
         (minCount,MaxCount)= solution[trait]
         if tag.group() == 'table':
            query="""SELECT atable FROM GeneticTemp WHERE pageID = """+str(pageID)
         else:
            query="""SELECT """+tag.group()+""" FROM GeneticTemp WHERE pageID = """+str(pageID)
         tagCount = connection.getOne(query)
         if tagCount:
            if tagCount[0] <=MaxCount and tagCount[0]>= minCount:
               count +=1
      if count/len(solution.keys()) > int(fitness):
         positive.append(pageID)
      else:
         negative.append(pageID)
   print(positive,' ',negative)
   query = """SELECT pageID FROM webpages WHERE pageType = 'test' AND siteID = """+str(siteID)
   results = connection.getAll(query)
   sitePages =[]
   for result in results:
      sitePages.append(result[0])
   print(sitePages)
   TP=0
   FP=0
   TN=0
   FN=0
   for pageID in positive:
      if pageID in sitePages:
         TP+=1
      else:
         FP+=1
   for pageID in negative:
      if pageID not in sitePages:
         TN+=1
      else:
         FN+=1
   print("TP: ",TP," TN: ",TN," FP: ",FP," FN: ",FN)
         
   accuracy = (TP+TN)/(TP+TN+FP+FN)
   print(accuracy)
   return accuracy
 
################################################################################
# Title:         geneticAlgorthm 
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   Porcess for implementing a genetic algorithm
# Arguments:     testID, webpage stats
# Sub-processes: randomSolutionGen, fitness, ranking, combination, mutation
################################################################################

def geneticAlgorithm(connection,testID):
   print("This is the geneticAlgorithm process")
   traitLists= {}
   query = """SELECT configID FROM tests WHERE testID = """+str(testID)
   result = connection.getOne(query)
   configID = result[0]
   query = """SELECT solutionNumber,generations,combinationFunc,rankingFunc,mutationFunc,fitnessFunc\
               FROM geneticAlgorithm WHERE configID = """+str(configID)
   (solutionNumber,generations,combination,ranking,mutation,fitness) = connection.getOne(query)
   query = """SELECT distinct args FROM traitList WHERE traitID = (SELECT traitID FROM traitList WHERE\
                                                       method = 'GeneticAlgorithm' AND \
                                                       configID ="""+str(configID)+""")"""
   traitList = connection.getAll(query)
   # get the maximum and minimum for each tagCount in test
   query = """SELECT min(count), max(count) FROM tagCount WHERE tagString = '"""
   for trait in traitList:
      innerQuery= query+trait[0]+"""'"""
      (minCount,maxCount)=connection.getOne(innerQuery)
      traitLists[trait[0]] = (minCount,maxCount)
   # build the random solutions
   # get the number of sites in the test
   query = """SELECT siteID FROM webSiteSamples WHERE testID = """+str(testID)
   siteIDs = connection.getAll(query)
   # create a sql table to hold relevant page data
   solutions = randomSolutionGen(solutionNumber,traitLists)
   (siteStats,pageIDList) = createTempTable(connection,traitList,siteIDs,solutions)
   pageIDList = []
   testPageList = []
   # get the sample pages for building the model
   query = """SELECT pageID,pageType FROM webpages WHERE siteID = """
   for siteID in siteIDs:
      innerQuery = query + str(siteID[0])
      results = connection.getAll(innerQuery)
      for result in results:
         (pageID,pageType) = result
         if pageType == 'sample':
            pageIDList.append(pageID)
         else:
            testPageList.append(pageID)
   for siteID in siteIDs:
      solutions = randomSolutionGen(solutionNumber,traitLists)
      for x in range(generations):
         solutionFitnesses = fitnessProcess(connection,solutions,fitness,siteID[0],pageIDList)
         solutions = rankingProcess(solutionFitnesses)
         if solutionFitnesses[1][0] >=.9:
            break
         combinationProcess(solutions,siteStats[siteID[0]])
         mutationProcess(solutions)
      # Save the top solution
      signature = ''
      solution = solutions[0]
      tagList = []
      for key in solution:
         tag =re.search(r'[a-z]+',key)
         if tag.group() == 'table':
            signature += ' atable '+str(solution[key][0])+' '+str(solution[key][1])            
         else:
            signature += ' '+tag.group()+' '+str(solution[key][0])+' '+str(solution[key][1])
      accuracy = testSolution(connection,solutions[0],fitness,siteID[0],testPageList)
      query = """INSERT INTO signatures(testID,siteID,solution,rank,accuracy) \
                 VALUES (:testID,:siteID,:signature,:rank,:accuracy)"""
      connection.query(query,(testID,siteID[0],signature,solutionFitnesses[1][0],accuracy))
 
   # remove the temp table
   query = """DROP TABLE GeneticTemp"""
   connection.getOne(query)
   return "success"


#connection = GeneralProcesses.sql()
#geneticAlgorithm(connection,16)
