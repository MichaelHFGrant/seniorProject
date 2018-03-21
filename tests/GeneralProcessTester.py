#! usr/bin/python3.5

import GeneralProcesses, sqlite3


configID = 1
# test

query = ("SELECT * FROM Samples")
connection = GeneralProcesses.sql()
result = connection.query(query)
print(result)
result = connection.query(query)
print(result)

query = "SELECT * FROM samples WHERE configID = " + str(configID)
print(query)

result = connection.query(query)
print(result)
    
