#! /usr/bin/puthon3.5

#  test module for Parser.py


import GeneralProcesses, sqlite3, Parser

testID = 5
connection = GeneralProcesses.sql()

Parser.Parser(connection,testID)
connection.commit(connection)
connection.close(connection)
