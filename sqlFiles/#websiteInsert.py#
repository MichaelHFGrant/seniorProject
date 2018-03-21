#! usr/bin/python3.5

#######################################################################
#   websiteInsert
#   places website URL's into the database
#######################################################################
import sqlite3

def websiteInsert(connection):

    curser = connection.execute("SELECT COUNT(*) FROM websiteList")
    result = curser.fetchone()
    siteNo = result[0]+1
    fHandle = open('txtbin/websites.txt')
    for line in fHandle:
        URL = line.strip()
        connection.execute("INSERT INTO websiteList (siteNo,\
                                                URL)\
                                    VALUES ('%d','%s')"%(siteNo,URL))
        siteNo +=1

#connection = sqlite3.connect('../database/csci491')
#websiteInsert(connection)
#connection.commit()
#connection.close()
