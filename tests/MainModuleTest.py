########################################################################################
# Title:         Main Module tester 
# Author:        Michael Grant   
# Date:          Oct 2017
# Description:   test scripts for testing the main module
# Arguments:     database connecton, testID
# Sub-processes: none
# Return Value:  Success or error message
########################################################################################

import GeneralProcesses, MainModule


def websiteAquisitionTest(connection,testID):
    websites = websiteAquisition(connection,testID)
    print(websites)





def mainTest():
    connection = GeneralProcesses.sql()
    testID = 1
    MainModule.websiteAquisition(connection,testID)

mainTest()
