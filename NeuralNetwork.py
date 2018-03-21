################################################################################
# Title:         NeuralNetwork 
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   Implements the neural network method of stylometric analysis
# Arguments:     testID, website statistics
# Sub-processes: tuning
################################################################################

import GeneralProcesses,re,random,math



################################################################################
# Title:         tuning 
# Author:        Michael Grant
# Date:          Sept 2017
# Description:   Changes the weights of the network according to the learning
#                function
# Arguments:     output error, learning function, layer sensitivities
# Sub-processes: none
################################################################################






def networkInit(connection,testID):
   configID = connection.getConfig(testID)
   #get the traits
   query = """SELECT distinct traitID FROM traitList WHERE configID = """+str(configID)
   traitIDs = connection.getAll(query)
   traitList = []
   for traitID in traitIDs:
      query = """SELECT args FROM traitList WHERE method = 'NeuralNetwork' and traitID = """+str(traitID[0])
      traits = connection.getAll(query)
      for trait in traits:
         traitList.append(trait[0])
   # get the sample sites
   query = """SELECT siteID FROM websiteSamples WHERE type = 'sample' AND testID = """+str(testID)
   siteIDs = connection.getAll(query)
   # get the webpage
   pageIDList = []
   siteIDList = []
   query = """SELECT pageID FROM webpages WHERE pageType = 'test' AND siteID = """ 
   for siteID in siteIDs:
      siteIDList.append(siteID[0])
      innerQuery = query + str(siteID[0])
      pageIDs = connection.getAll(innerQuery)
      for pageID in pageIDs:
         pageIDList.append(pageID[0])
   # build the tempTable
   GeneralProcesses.createTempTable(connection,testID,traitList,'NeuralNetwork')
   return (traitList,siteIDList,pageIDList)


def tuneNetwork(connection,testID,inputLayer,hiddenLayer,outputLayer,pageIDs):
   pageID = random.choice(pageIDs)
   output =inputLayer.getOutputs(connection,pageID)
   output = hiddenLayer.getOutputs(output)
   output = outputLayer.getOutputs(output)
   
   errors = outputLayer.getError(connection,pageID)
   total =0
   for err in errors:
      total += abs(errors[err])
   sense,weight =outputLayer.updateSensitivitys()
   sense,weight =hiddenLayer.updateSensitivitys(sense,weight)
   inputLayer.updateSensitivitys(sense,weight)
   outputLayer.updateWeights()
   hiddenLayer.updateWeights()
   inputLayer.updateWeights()
   return total


def testNetwork(connection,testID,inputLayer,hiddenLayer,outputLayer):
   # get the sample pages for the test
   query = """SELECT siteID FROM websiteSamples WHERE testID = """+str(testID)
   siteIDs = connection.getAll(query)
   query = """SELECT pageID FROM webpages WHERE pageType = 'test' AND siteID = """
   pageIDs = []
   for siteID in siteIDs:
      innerQuery = query + str(siteID[0])
      total = 0
      pageIDs = connection.getAll(innerQuery)
      for pageID in pageIDs:
         output =inputLayer.getOutputs(connection,pageID[0])
         output = hiddenLayer.getOutputs(output)
         output = outputLayer.getOutputs(output)
         errors = outputLayer.getError(connection,pageID[0])
         for error in errors.keys():
            total+=abs(int(errors[error]))
      insertQuery = """INSERT INTO networkResults (testID,siteID,error) VALUES(:testID,:siteID,:total)"""
      connection.query(insertQuery,(testID,siteID[0],total))


def neuralNetwork(connection,testID):
   print("This is the neuralNetwork process")
   # get the init configuration
   (traitList,siteIDs,pageIDs) = networkInit(connection,testID)
   # configure the network
   inputLayer = InputLayer(connection,testID,traitList)
   hiddenLayer = HiddenLayer(connection,testID,traitList)
   outputLayer = OutputLayer(connection,testID,traitList,siteIDs)
   error = 2
   count = 0
   while error >=1 and count <10000:
      error = tuneNetwork(connection,testID,inputLayer,hiddenLayer,outputLayer,pageIDs)
      count+=1
   testNetwork(connection,testID,inputLayer,hiddenLayer,outputLayer)

class Neuron():
   def __init__(self,inputSize):

      self.inputSize = inputSize
      self.output = 0
    
      self.bias = 1
      self.N = 0
      self.sensitivity = 0


   def calculateN(self,inputs,weights):
      self.N = self.bias
      for x in range(self.inputSize):
         self.N+= weights[x]*inputs[x]
      
      return self.N
   
   def getOutput(self,Function):
      transferFunction = compile(Function,"string","exec")
      exec(transferFunction)
      
      return self.output

   def returnOutput(self):
      return self.output


   def setSensitivity(self,sense):
      self.sensitivity = sense
   
   def updateSensitivity(self,Function,error,weights=None):
      self.sensitivity = 0
      backPropagation = compile(Function,"string","exec")
      for x in error.keys():
         exec(backPropagation)

   def getSensitivity(self):
      return self.sensitivity

   
   def printAll(self):
      print("inputSize  : ",self.inputSize)
      print("output     : ",self.output)
      print("inputs     : ",self.inputs)
      print("bias       : ",self.bias)
      print("N          : ",self.N)
      print("sensativity: ",self.sensitivity)

      

class InputLayer():
   def __init__(self,connection,testID,traitList):
      print("This is the input layer")
      # get the configID
      configID = connection.getConfig(testID)
      query = """SELECT inputLayerTF, inputLayerBPF FROM neuralNetwork WHERE configID = """+str(configID)
      self.transfer,self.backPropigation = connection.getOne(query)
      self.inputNeuron = {}
      self.traitList = traitList
      self.weights = {}
      self.learningRate = .01
      hiddenLayerRatio = .7
      configID = connection.getConfig(testID)
      self.traitListLength = len(traitList)
      for trait in traitList:
         self.inputNeuron[trait]=Neuron(1)
         weights = []
         for x in range(int(float(len(traitList))*hiddenLayerRatio+1)):
            weights.append(random.uniform(0,1))
         self.weights[trait]=weights

   def getOutputs(self,connection,pageID):
      outputs = []
      for trait in self.traitList:
         inputs = []
         inputs.append(connection.getData(trait,pageID,'NeuralNetwork'))
         N = self.inputNeuron[trait].calculateN(inputs,self.weights[trait])
         outputs.append(self.inputNeuron[trait].getOutput(self.transfer))
      return outputs

   
   def updateSensitivitys(self,sensitivitys,weights):
      x=0
      for trait in self.traitList:
         temp = 0
         output = self.inputNeuron[trait].returnOutput()
         for y in weights.keys():
            temp+=weights[y][x]*sensitivitys[y]*(1-output)*output
         self.inputNeuron[trait].setSensitivity(temp)
         x+=1


   def updateWeights(self):
      for x in self.weights.keys():
         for weight in range(len(self.weights[x])):
            self.weights[x][weight]-= self.learningRate*self.weights[x][weight]*self.inputNeuron[x].getSensitivity()
      
         
class HiddenLayer():

   def __init__(self,connection,testID,traitList):
      print("This is the hidden Layer")
      # get the configID
      configID = connection.getConfig(testID)
      query = """SELECT hiddenLayerTF, hiddenLayerBPF FROM neuralNetwork WHERE configID = """+str(configID)
      self.transfer,self.backPropigation = connection.getOne(query)

      
      pageIDs = connection.getPageIDs(testID)
      self.hiddenNeuron = {}
      self.traitList = traitList
      self.weights = {}
      self.sensitivitys = {}
      self.learningRate = .01
      hiddenLayerRatio = .5
      configID = connection.getConfig(testID)
      self.layerSize = int(float(len(traitList))*hiddenLayerRatio+1)
      for x in range(int(float(len(traitList))*hiddenLayerRatio+1)):
         self.hiddenNeuron[x]=Neuron(len(traitList))
         weights = []
         for y in range(len(traitList)):
            weights.append(random.uniform(0,1))
         self.weights[x]=weights
         
   def getOutputs(self,inputs):
      outputs = []
      for x in range(self.layerSize):
         N = self.hiddenNeuron[x].calculateN(inputs,self.weights[x])
         outputs.append(self.hiddenNeuron[x].getOutput(self.transfer))
      return outputs      


   def updateSensitivitys(self,sensitivitys,weights):
      backPropigation = compile(self.backPropigation,"string","exec")
      for x in range(self.layerSize):
         temp = 0
         for y in weights.keys():
            output = self.hiddenNeuron[x].returnOutput()
            temp+=weights[y][x]*sensitivitys[y]*(1-output)*output
         self.hiddenNeuron[x].setSensitivity(temp)
         self.sensitivitys[x]=temp
      return (self.sensitivitys,self.weights)



   def updateWeights(self):
      for x in self.weights.keys():
         for weight in range(len(self.weights[x])):
            self.weights[x][weight]-= self.learningRate*self.weights[x][weight]*self.hiddenNeuron[x].getSensitivity()

  




class OutputLayer():

   def __init__(self,connection,testID,traitList,siteIDs):
      print("This is the output Layer")
      # get the configID
      configID = connection.getConfig(testID)
      query = """SELECT outputLayerTF, outputLayerBPF FROM neuralNetwork WHERE configID = """+str(configID)
      self.transfer,self.backPropigation = connection.getOne(query)
      self.transfer="""
if self.N > 1:
   self.output=1
else:
   self.output=0"""
      self.learningRate = .01
      self.outputNeuron = {}
      self.backPropigation ="""self.sensitivity = (-2)*(1/self.N)*error[x]"""
      self.traitList = traitList
      self.weights = {}
      self.errors = {}
      self.outputs={}
      hiddenLayerRatio = .5
      configID = connection.getConfig(testID)
      siteIDs.append('RH')
      self.siteIDs = siteIDs
      for siteID in self.siteIDs:
         self.outputNeuron[siteID]=Neuron(int(float(len(traitList))*hiddenLayerRatio+1))
         weights = []
         self.errors[siteID]=0
         for y in range(int(float(len(traitList))*hiddenLayerRatio+1)):
            weights.append(random.uniform(0,1))
         self.weights[siteID]=weights

         
   def getOutputs(self,inputs):
      outputs = []
      for siteID in self.siteIDs:
         N = self.outputNeuron[siteID].calculateN(inputs,self.weights[siteID])
         self.outputs[siteID] = self.outputNeuron[siteID].getOutput(self.transfer)
         
         outputs.append(self.outputs[siteID])
      return outputs  



   def getError(self,connection,pageID):
      # get the siteID which the pageID belongs
      query = """SELECT siteID FROM webpages WHERE pageID = """+str(pageID)
      targetSite = connection.getOne(query)
      
      for siteID in self.outputNeuron.keys():
         if siteID == targetSite[0]:
            self.errors[siteID] = 1-self.outputNeuron[siteID].returnOutput()
         elif targetSite[0] in self.siteIDs:
            self.errors[siteID] = -self.outputNeuron[siteID].returnOutput()
         else:
            self.errors['RH'] = (1-self.outputNeuron[siteID].returnOutput())
      return self.errors

   def updateSensitivitys(self):
      sensitivity = {}
      for siteID in self.siteIDs:
         error = {}
         error[siteID]=self.errors[siteID]
         self.outputNeuron[siteID].updateSensitivity(self.backPropigation,error)
         sensitivity[siteID]=self.outputNeuron[siteID].getSensitivity()
      return (sensitivity,self.weights)


   def updateWeights(self):
      for siteID in self.weights.keys():
         for x in range(len(self.weights[siteID])):
            self.weights[siteID][x]-= self.learningRate*self.weights[siteID][x]*self.outputNeuron[siteID].getSensitivity()

#connection=GeneralProcesses.sql()
#neuralNetwork(connection,5)
