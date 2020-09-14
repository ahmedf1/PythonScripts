'''
    This script will be the main page for the processes that opens the gui for
    each process depending on which is clicked. Functionality for EDFDump is
    already in place. This will to additionaly functionality being added for
    RepCalcs and BuildTheBank Processes.


    will have to remove the view dashboard button from the edfdump gui
    since that should be more of a thing that goes in this view
'''

from tkinter import *   
import time
import datetime
import EDFDump_GUI
import RepCalcs_GUI
import viewLogsDashboard
from functools import partial

class Clock:
    def __init__(self):
        self.time1 = ''
        self.time2 = time.strftime('%I:%M:%S %p')
        self.mFrame = Frame()
        self.mFrame.pack(side=TOP,expand=YES,fill=X)
        self.date = Label(self.mFrame, text=str(datetime.date.today()), font=('times',15,'bold'))
        self.watch = Label(self.mFrame, text=self.time2, font=('times',15,'bold'))
        self.date.pack()
        self.watch.pack()
    
        self.changeLabel() #first call it manually

    def changeLabel(self): 
        self.time2 = time.strftime('%I:%M:%S %p')
        self.watch.configure(text=self.time2)
        self.mFrame.after(200, self.changeLabel) #it'll call itself continuously


    
def buildRealTimeClock():
    obj1 = Clock()

def buildRepCalcs(bottomFrame):
    Button(bottomFrame, text = "View RepCalcs", relief = RIDGE, font=("Courier",22), width = 20, height = 2, command = partial(RepCalcs_GUI.main)).grid(row = 0, column=1)    

def buildEDFDump(bottomFrame):
    # just make a button and then make the command to open/run the gui for edfdump
    openEDFDumpGUI = partial(EDFDump_GUI.main)
    Button(bottomFrame, text = "View EDFDump", relief = RIDGE, font=("Courier",22), width = 20, height = 2, command = openEDFDumpGUI).grid(row = 0, column=0)

def buildBTB(bottomFrame):
    Button(bottomFrame, text = "View BuildTheBank", relief = RIDGE, font=("Courier",22), width = 20, height = 2).grid(row = 0, column=2)
     
def buildGUI():
    root = Tk()
    root.resizable(width=False, height=False)
    topFrame = Frame(root)
    
    processName = Label(topFrame, text ='Vantage Commodities Processes', relief = RIDGE, font=("Courier",22), width=60)
    processName.pack()
    processName.pack(fill="x", expand=True, in_= topFrame)
    topFrame.pack()

    buildRealTimeClock()
    
    viewDashFrame = Frame(topFrame)
    viewDashFrame.pack(side = BOTTOM)
    viewDash = Button(viewDashFrame, text = "View Dashboard",relief = RIDGE, font=("Courier",22), width =60, height = 2, wraplength=160, command = partial(viewLogsDashboard.main))   
    viewDash.pack(fill="x", expand=True, in_= viewDashFrame, side = BOTTOM)
    viewDashFrame.pack()
    
    bottomFrame = Frame(root)
    
    buildEDFDump(bottomFrame)
    buildRepCalcs(bottomFrame)
    buildBTB(bottomFrame)

    bottomFrame.pack(side = BOTTOM)    
    root.mainloop()
    
def main():
    buildGUI()


main()


