'''
this script is designed to query the APX2000 database and retreive active
clients so that they can be cross referenced with the RepCalcs Contracts Log
File in another script to make sure the daily execution of the program was
successful
qa-sqlp-a01
'''

import pyodbc
import datetime

def getActiveClientsFromDB():

    cnxn = pyodbc.connect('Driver={SQL Server};'
                            'Server=10.50.13.30;'
                            'Database=APX2000;'
                            'Trusted_Connection=True;')
    cursor = cnxn.cursor()
    activeRepswithRecv = [46,41,85]
    dateToday = datetime.date.today()
    PTD = str(dateToday.year) + '-' + str(dateToday.month) + '-' + str(dateToday.day) + " 03:59:59"
    print(PTD)
    activeClients = []
    for repID in activeRepswithRecv:
        BilledQuery = "SELECT TOP (10) * FROM [APX2000].[dbo].[clr_RepGenBilled] WHERE RepId = " + str(repID) + " AND ProcessThruDate = '" + PTD + "'"
        UnBilledQuery = "SELECT TOP (10) * FROM [APX2000].[dbo].[clr_RepGenUnBilled] WHERE RepId = " + str(repID) + " AND ProcessThruDate = '" + PTD + "'"
        cursor.execute(BilledQuery)
        
        while 1:
            row = cursor.fetchone()
            if not row:
                break
            activeClients.append(row[0])
            #print(row)
        if len(activeClients) == 10:
            # successful insert
            print("Successful Billed insert for ", repID)
        activeClients = []
        cursor.execute(UnBilledQuery)
        
        while 1:
            row = cursor.fetchone()
            if not row:
                break
            activeClients.append(row[0])
            #print(row)
        if len(activeClients) == 10:
            # successful insert
            print("Successful UnBilled insert for ", repID)
        activeClients = []
    cnxn.close()
    return activeClients

    


getActiveClientsFromDB()
