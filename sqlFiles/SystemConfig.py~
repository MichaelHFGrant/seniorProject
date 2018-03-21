#! usr/bin/python3.5

import sqlite3, configInsert, CreateSystemDataTables,websiteInsert,traits,TransferBackpropigation

    
def createTables(connection):
    print("This is createTables")
    connection.execute('CREATE TABLE IF NOT EXISTS configuration(\
                                     configID INTEGER NOT NULL UNIQUE,\
                                     configCreator INTEGER NOT NULL,\
                                     configDate  INTEGER NOT NULL,\
                                     PRIMARY KEY (configID))')
    
    connection.execute('CREATE TABLE IF NOT EXISTS samples(\
                                     websiteSampleSize INTEGER NOT NULL,\
                                     webpageSampleSize INTEGER NOT  NULL,\
                                     redherringSize    INTEGER NOT NULL,\
                                     configID   INTEGER NOT NULL,\
                                     FOREIGN KEY (configID) REFERENCES configuration(configID))')


    connection.execute('CREATE TABLE IF NOT EXISTS traits(\
                                     traitID INTEGER NOT NULL UNIQUE,\
                                     Ngram INTEGER,\
                                     RExp    BLOB NOT NULL,\
                                     testCode BLOB  NOT NULL,\
                                     PRIMARY KEY (traitID))')
                       
    connection.execute('CREATE TABLE IF NOT EXISTS traitList(\
                                     traitID INTEGER NOT NULL,\
                                     method  TEXT NOT NULL,\
                                     args    BLOB,\
                                     condition BLOB,\
                                     statTest BLOB NOT NULL,\
                                     configID INTEGER NOT NULL,\
                                     FOREIGN KEY (configID) REFERENCES configuration(configID))')
                       
    connection.execute('CREATE TABLE IF NOT EXISTS IntermediateParser(\
                                     IMRExp  BLOB NOT NULL,\
                                     dataType VARCHAR(1),\
                                     configID int,\
                                     FOREIGN KEY (configID) REFERENCES configuration(configID))')

    connection.execute('CREATE TABLE IF NOT EXISTS rarePairs(\
                                     maxNgram INTEGER NOT NULL,\
                                     configID int,\
                                      FOREIGN KEY (configID) REFERENCES configuration(configID))')

    connection.execute('CREATE TABLE IF NOT EXISTS writerInvariant(\
                                     configID INTEGER,\
                                     FOREIGN KEY (configID) REFERENCES configuration(configID))')

    connection.execute('CREATE TABLE IF NOT EXISTS geneticAlgorithm(\
                                     solutionNumber INTEGER NOT NULL,\
                                     generations     INTEGER NOT NULL,\
                                     combinationFunc TEXT NOT NULL,\
                                     rankingFunc     TEXT NOT NULL,\
                                     mutationFunc    TEXT NOT NULL,\
                                     fitnessFunc     INTEGER NOT NULL,\
                                     configID        INTEGER,\
                                     FOREIGN KEY (configID) REFERENCES configuration(configID))')


    connection.execute('CREATE TABLE IF NOT EXISTS neuralNetwork(\
                                     hiddenLayerRatio NOT NULL,\
                                     InputLayerTF BLOB NOT NULL,\
                                     HiddenLayerTF BLOB NOT NULL,\
                                     outputLayerTF BLOB NOT NULL,\
                                     inputLayerBPF Blob NOT NULL,\
                                     hiddenLayerBPF BLOB NOT NULL,\
                                     outputLayerBPF BLOB NOT NULL,\
                                     learningRate INTEGER NOT NULL,\
                                     convergenceFunc TEXT NOT NULL,\
                                     configID INTEGER NOT NULL,\
                                     FOREIGN KEY (configID) REFERENCES configuration(configID))')                                   

    connection.execute('CREATE TABLE IF NOT EXISTS layers(\
                                     layerType  varchar(1) NOT NULL,\
                                     layerSizeFunc TEXT NOT NULL,\
                                     transferFunc  TEXT NOT NULL,\
                                     backPropFunc  TEXT NOT NULL,\
                                     nnID       INTEGER ,\
                                     FOREIGN KEY (nnID) REFERENCES neuralNetwork(nnID))')
    return "success"


def main():
   print("main")
   connection = sqlite3.connect('../database/csci491')
   configID = 1
   # create the needed tables for system configuration if they do not exist
   status = createTables(connection)

   # insert configuration table data
   fHandle = open('tableUpdates.txt')
   for line in fHandle:
       Cfile = line.rstrip()
       table = line.split('.',1)
       print(table[0])
       status = configInsert.configInsert(connection,Cfile,table[0])

   CreateSystemDataTables.createTables(connection)
   websiteInsert.websiteInsert(connection)
   traits.main(connection)                                
   TransferBackpropigation.transferFunctions(connection,configID)
   connection.commit()
   connection.close()


main()
