'''
    This script will be used to extract relevant rows from the dashboard and
    display them on the gui so that there is no need to even open the google
    sheets via web browser. Includes a refresh button to ensure latest results
    are being retrieved. 
'''

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
#from oauth2client import file, client, tools
import datetime
import os
from tkintertable import *
from tkinter import *
import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


#define where the credentials file is located
#used to authenticate connection to sheets
# custom file made by google api
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= r"C:\Users\fahmed\Desktop\ML for Logs\credentials.json"



def getDashboardDataFromSheetsAPI():
    # If modifying these scopes, delete the file token.json.
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'

    # The ID of spreadsheet.
    SPREADSHEET_ID = '1Un9xW2lkNSpoGykg0giTxJgpVVK9h7xQSw4brjEhq9k'

    # This cell in this sheet contains the address of the cell that contains the ptd
    PTD_Cell_Address = 'Morning!J61'

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

    # now create the range of the rows we want to extract
    # for now just get the ptd and previous 10 days

    # sheet name: Morning
    # row number of the ptd: rowNumberofPTD
    # columns we need: A -> F
    # so now build the range
    
    rowNumber10DaysAgo = str(int(rowNumberofPTD) - 10)
    rangePast10days = 'Morning!A' + (rowNumber10DaysAgo) + ':F' + rowNumberofPTD
    request = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=rangePast10days)
    response = request.execute()
    return response["values"]

def setupDashboardTitles(dashboardObj, TitleSection):
    dashboardObj.title("Vantage Daily Log Reports Dashboard")
    dashboardTitle = Label(dashboardObj, text = "Vantage Daily Log Reports Dashboard", relief = RIDGE, font=("Courier",22),width=50, height = 2, padx = 50)
    dashboardTitle.pack(in_ = TitleSection, side = TOP)



def yete():
    #dashboard = Toplevel()
    dashboard = Tk()
    TitleSection = Frame(dashboard)
    dataSection = Frame(dashboard)
    TitleSection.pack(side = TOP)
    dataSection.pack(side = BOTTOM, fill = 'both', expand = True)

    setupDashboardTitles(dashboard, TitleSection)

    dashboardData = getDashboardDataFromSheetsAPI()
    DashboardsheetValues = dashboardData["values"]
    print(DashboardsheetValues)
    
    table = TableCanvas(dataSection)
    table.show()
    
class App(QWidget):
 
    def __init__(self):
        super().__init__()
        self.title = 'Vantage Daily Logs Dashboard'
        self.left = 600
        self.top = 300
        self.width = 700
        self.height = 400
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
 
        self.createTable()
 
        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget) 
        self.setLayout(self.layout) 
 
        # Show widget
        self.show()

    def createTableCellItem(self,data):
        itemtoInsert = QTableWidgetItem(str(data))
        if str(data) == 'Success':
            itemtoInsert.setBackground(QtGui.QColor(144, 238, 144))
        elif str(data) == 'Small Issue':
            itemtoInsert.setBackground(QtGui.QColor(240,230,140))
        return itemtoInsert
        
    
    def createTable(self):
       # Create table
        data = getDashboardDataFromSheetsAPI()
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(11)
        self.tableWidget.setColumnCount(6)
        rowNum = 0
        for i in range(0, len(data)):
            self.tableWidget.setItem(i,0, self.createTableCellItem(data[i][0]))
            self.tableWidget.setItem(i,1, self.createTableCellItem(data[i][1]))
            self.tableWidget.setItem(i,2, self.createTableCellItem(data[i][2]))
            self.tableWidget.setItem(i,3, self.createTableCellItem(data[i][3]))
            self.tableWidget.setItem(i,4, self.createTableCellItem(data[i][4]))
            self.tableWidget.setItem(i,5, self.createTableCellItem(data[i][5]))
            #self.tableWidget.setItem(3,0, QTableWidgetItem("Cell (4,1)"))
            #self.tableWidget.setItem(3,1, QTableWidgetItem("Cell (4,2)"))
        self.tableWidget.move(0,0)
        self.tableWidget.setHorizontalHeaderLabels(["PTD", "PRD: EDFDump", "PRD: RepCalcs", "QA: EDFDump", "QA: RepCalcs", "BuildTheBank"]) 
        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)
 
    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
def main():
    app = QApplication(sys.argv)
    ex = App()
    app.exec_()


