

import sqlite3



def transferFunctions(connection,configID):
    configList = []
    
    Cfile = open('NeuralConfig.txt')
    for line in Cfile:
        print(line)
        function = ''
        configList = line.split()
        name =configList.pop(0)
        for x in range(len(configList)):
            function += configList[x]+' '
        print(name,' ',function)

        query = """UPDATE NeuralNetwork SET """+name+"""= """+function+""" WHERE configID = """+str(configID)
        connection.execute(query)
        print(query)



connection = sqlite3.connect('../database/csci491')
transferFunctions(connection,1)
connection.commit()
connection.close()
