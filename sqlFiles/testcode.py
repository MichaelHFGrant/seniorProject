#! usr/bin/python3.5

#    connection.execute('CREATE TABLE IF NOT EXISTS configuration(\
 #                                    configID INTEGER NOT NULL UNIQUE,\
  #                                   websiteSample INTEGER NOT NULL,\
   #                                  webpageSample INTEGER NOT NULL,\
    #PRIMARY KEY (configID))')
import MySQLdb

def test(connection):
    configID = 2
    wSample = 20
    pSample = 20

    sqlInsert = "INSERT INTO configuration(configID,websiteSample,webpageSample)\
                                    VALUES('%d', '%d', '%d')"%\
                                    (configID,wSample,pSample)
    
    connection.execute(sqlInsert)
    

def main():

   DB = MySQLdb.connect(host="localhost",
                              user="michael",
                              passwd="Fritz",
                              db="csci491")
   connection = DB.cursor()
   test(connection)
   DB.commit()

main()
