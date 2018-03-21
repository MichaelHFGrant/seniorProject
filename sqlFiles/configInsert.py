


def configInsert(connection,file,table):
    print("This is configInsert")
    IDquery = "SELECT COUNT(*) FROM %s" %(table)
    Cfile = open(file)
    arguments = ()

    for line in Cfile:
        row = line.split()
        curser = connection.execute(IDquery)
        result = curser.fetchone()
        configID= result[0]+1
        if (table == 'configuration'):
            wSample = row[0]
            pSample = row[1]
            insertRow = "INSERT INTO configuration(configID,configCreator,configDate)\
                                VALUES('%d','%s','%s')"%(configID,wSample,pSample)

        if (table == 'samples'):
            wSample = row[0]
            pSample = row[1]
            hSample = row[2]
            insertRow = "INSERT into samples(websiteSampleSize,webpageSampleSize,\
                                             redherringSize,configID)\
                                VALUES('%s','%s','%s','%d')"%(wSample,pSample,hSample, configID)
            
        if (table == 'traits'):
            RX = row[0]
            Tcode = row[1]
            CID = row[2]
            insertRow = "INSERT INTO traits(traitID,RExp,testCode,confidID)\
                                     VALUES('%d','%s','%s','%s')"%(configID,RX,Tcode,CID)

        if (table == 'IntermediateParser'):
            IMRX = row[0]
            Dtype = row[1]
            CID = row[2]
            insertRow = """INSERT INTO IntermediateParser(IMRExp,dataType,configID)\
                                VALUES(:IMRX,:Dtype,:CID)"""
            arguments = (IMRX,Dtype,CID)
            

        if (table =='GeneticAlgorithm'):
            solutionNumber = row[0]
            generations = row[1]
            combinationFunc = row[2]
            rankingFunc = row[3]
            mutationFunc = row[4]
            fitnessFunc = row[5]
            configID = row[6]
            insertRow = """INSERT INTO GeneticAlgorithm(solutionNumber,generations,combinationFunc,\
                                                  rankingFunc,mutationFunc,fitnessfunc,configID)\
                                VALUES(:solutionNumber,:generations,:combinationfunc,:rankingFunc,:mutationFunc,:fitnessFunc,\
                                       :configID)"""
            arguments = (solutionNumber,generations,combinationFunc,rankingFunc,mutationFunc,fitnessFunc,configID)

        
        if (table =='NeuralNetwork'):
            hiddenLayerRatio = row[0]
            inputLayerTF = row[1]
            hiddenLayerTF = row[2]
            outputLayerTF = row[3]
            inputLayerBPF = row[4]
            hiddenLayerBPF= row[5]
            outputLayerBPF = row[6]
            learningRate = row[7]
            convergenceFunc = row[8]
            configID = row[9]
            insertRow = """INSERT INTO NeuralNetwork(\
            hiddenLayerRatio,InputLayerTF,HiddenLayerTF,\
            outputLayerTF,inputLayerBPF,hiddenLayerBPF,\
            outputLayerBPF,learningRate,convergenceFunc,\
            configID)
            VALUES (:hiddenLayerRatio,:InputLayerTF,:HiddenLayerTF,\
            :inputLayerTF,:inputLayerBPF,:hiddenLayerBPF,\
            :outputLayerBPF,:learningRate,:convergenceFunc,\
            :configID)"""
            arguments = (hiddenLayerRatio,inputLayerTF,hiddenLayerTF,\
            inputLayerTF,inputLayerBPF,hiddenLayerBPF,\
            outputLayerBPF,learningRate,convergenceFunc,\
            configID)
            
        
        connection.execute(insertRow,arguments)
