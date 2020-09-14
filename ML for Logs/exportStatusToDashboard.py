'''
    The main function within this file is called from within the ML algorithm
    file to insert process results into the dashboard. Since the dashboard
    is hosted on google sheets, this script connects to the google sheet via
    api.
    
    Requires:
    credentials.json file distributed by google api for authentication purposes
    
    Critical identifying Variables:
    Spreadsheet ID --> unique to each spreadsheet, specifes which sheet to edit
    Cell Address --> necessary to know which cells to update/get data from
    
'''


from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
import os

#define where the credentials file is located
#used to authenticate connection to sheets
# custom file made by google api
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= r"C:\Users\fahmed\Desktop\ML for Logs\credentials.json"

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = '1Un9xW2lkNSpoGykg0giTxJgpVVK9h7xQSw4brjEhq9k'
PTD_Cell_Address = 'Morning!J61'

# this function inserts the results of QA EdfDump into the Daily Logs dashboard
def insertPRDStatus(prdStatus,prdCellforInsert, sheet):
    PRDvalues = [
        [
            prdStatus
        ]
    ]

    PRDbody = {
        'values': PRDvalues
    }

    PRD_result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                               range=prdCellforInsert,valueInputOption="RAW", body=PRDbody).execute()

# this function inserts the results of QA EdfDump into the Daily Logs dashboard
def insertQAStatus(qaStatus,qaCellforInsert, sheet):
    QAvalues = [
        [
            qaStatus
        ]
    ]

    QAbody = {
        'values': QAvalues
    }

    QA_result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                               range=qaCellforInsert,valueInputOption="RAW", body=QAbody).execute()

# one of the parameters is ptd, this is for inserting results into weekend rows
    # manually
    # another parameter is boolean isManualUpdate to differentiate between an auto
    # insertion and a manual update
    
def main(prdStatus,qaStatus, ptd, isManualUpdate):
    
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('sheets', 'v4', http=creds.authorize(Http()))

    # Call the Sheets API
    sheet = service.spreadsheets()
    PTD_Cell = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID, range=PTD_Cell_Address).execute()
    numRows = PTD_Cell.get('values') if PTD_Cell.get('values')is not None else 0

    # gets the row number
    rowNumberofPTD = PTD_Cell['values'][0][0].split('$')[2]

    
    if isManualUpdate:
        year, month, day = (int(x) for x in ptd.split('-'))
        dayofWeek = datetime.date(year,month,day).weekday()
        if dayofWeek == 6:
            # this is sunday, so build the cell address for sunday
            # since the ptd on a manual update will be monday, just subtract 1
            # to get the row right above aka sunday
            rowNumberofPTD -= 1
        if dayofWeek == 5:
            # same as above, except here we are updating for saturday so
            # subtract 2
            rowNumberofPTD -= 2
            

    # now build the string for insertion
    # column B is for PRD
    prdCellforInsert = 'Morning!B' + rowNumberofPTD
    print(prdCellforInsert)
    
    # column D is for QA
    qaCellforInsert = 'Morning!D' + rowNumberofPTD
    print(qaCellforInsert)

    # if prdStatus is an empty string, this means this function is being called
    # from the gui and we only want to insert results for QA
    if (prdStatus == ""):
        insertQAStatus(qaStatus,qaCellforInsert, sheet)

    # if qaStatus is an empty string, this means this function is being called
    # from the gui and we only want to insert results for PRD
    elif (qaStatus == ""):
        insertPRDStatus(prdStatus,prdCellforInsert, sheet)

    # this is being called by the ML script when run from the task scheduler
    else:
    
        PRDvalues = [
            [
                prdStatus
            ]
        ]

        PRDbody = {
            'values': PRDvalues
        }

        QAvalues = [
            [
                qaStatus
            ]
        ]

        QAbody = {
            'values': QAvalues
        }

        
        PRD_result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                               range=prdCellforInsert,valueInputOption="RAW", body=PRDbody).execute()

        QA_result = sheet.values().update(spreadsheetId=SPREADSHEET_ID,
                               range=qaCellforInsert,valueInputOption="RAW", body=QAbody).execute()

    

    
if __name__ == '__main__':
    main(prdStatus, qaStatus, ptd, isManualUpdate)
