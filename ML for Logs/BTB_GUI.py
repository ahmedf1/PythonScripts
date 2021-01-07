'''

    This script builds the GUI interface for the BuildTheBank Process.
    Each process has its own log file and all teh files are currently in the
    same directory. However, the processes never do any directory cleaning and
    instead just append to the end of the log file. The functions in this script
    work to extract the process results from each of the files and display them.
    It also allows for viewing the results from previous PTD's.
'''

from tkinter import *
import os
import tkinter as tk
from datetime import *
from functools import partial
from tkcalendar import *



# functions for opening each of the files
# called depending on which file is selected for viewing

def tail(file, n=1, bs=1024):
    f = open(file, 'r')
    f.seek(0,2)
    l = 1-f.read(1).count('\n')
    B = f.tell()
    while n >= l and B > 0:
            block = min(bs, B)
            B -= block
            f.seek(B, 0)
            l += f.read(block).count('\n')
    f.seek(B, 0)
    l = min(l,n)
    lines = f.readlines()[-l:]
    f.close()
    return lines

def openBTBfile(ptd, filepath):
    # get 100 lines from the end of the file
    n=100

    # for Gas Invertory --> spans ~30 days --> which is 450 lines
    if filepath == r"\\prd-app-a01\d$\BuildTheBank\Logs\CalculateNaturalGasInventory.log": n = 450
    lines = tail(filepath,n)
    linestoReturn = []
    formattedPTD =  ptd.strftime('%#m/%d/%Y')
    
    for lineNumber in range(0, len(lines)):
        # first line is the one that contains the date we are looking for
        if formattedPTD in lines[lineNumber]:
            startLine = lineNumber
            break

    # if formattedPTD was not found, we create the formated PTD from the most recent PTD aka yesterday
    if 'startLine' not in locals():
        yesterdayPTD = (ptd - timedelta(1)).strftime('%#m/%d/%Y')
        for lineNumber in range(0, len(lines)):
            if yesterdayPTD in lines[lineNumber]:
                startLine = lineNumber
                break
    try:
        startLine
    except UnboundLocalError:
        print("DATA ERROR")
        linestoReturn.append("MALFORMED DATA -- CHECK FILE")
    else:
        for index in range(startLine, len(lines)):
            linestoReturn.append(lines[index])

    return linestoReturn
    

# takes the lines retreived from the log file and inserts into the GUI object, highlighting success indicators

def printLinesToListBox(lines, ListBoxOBJ):
    ListBoxOBJ.delete(0,END)
    index = 0
    for line in lines:
        ListBoxOBJ.insert(index, line)
        if 'Success' in line:
            ListBoxOBJ.itemconfig(index, bg = 'light green')
        index +=1

# simply jumps the date from a past one to the most recent PTD

def switchDateToToday(calendarOBJ):
    calendarOBJ.set_date(datetime.today())
    
# displays the process name who's file we are currently viewing

def displayBTBlog(ptd, processToDisplay, ListBoxOBJ):
    process = processToDisplay.get()
    print(process)
    lines = openBTBfile(ptd,process)
    printLinesToListBox(lines, ListBoxOBJ)

# puts together all the GUI elements

def buildBTBgui():
    root = Tk()
    root.resizable(width=False, height=False)
    topFrame = Frame(root)
    bottomFrame = Frame(root)
    LogSection = Frame(root)
    LogSection.pack(side = BOTTOM, fill='x', expand = False)
    
    processName = Label(topFrame, text ='BuildTheBank Logs', relief = RIDGE, font=("Courier",22), width=30)
    processName.pack(fill="x", expand=True, in_= topFrame)

    Label(topFrame, text='Choose date').pack(padx=10, pady=10)

    cal = DateEntry(topFrame, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
    cal.pack(padx=10, pady=10)
    Button(topFrame, text = "Jump to Today", command = partial(switchDateToToday, cal)).pack(padx=10, pady=10)


    
    BTBprocesses = [
        r"\\prd-app-a01\d$\BuildTheBank\Logs\CalculateEscoTaxObligations.log",
        r"\\prd-app-a01\d$\BuildTheBank\Logs\RefreshCapitalLedger.log",
        r"\\prd-app-a01\d$\BuildTheBank\Logs\CalculateTreasuryCompliance.log",
        r"\\prd-app-a01\d$\BuildTheBank\Logs\ImportBaiBankTransactions.log",
        r"\\prd-app-a01\d$\BuildTheBank\Logs\CalculateBorrowingBaseReserve.log",
        r"\\prd-app-a01\d$\BuildTheBank\Logs\ImportForwardPrices.log",
        r"\\prd-app-a01\d$\BuildTheBank\Logs\CalculateDailyInterest.log",
        r"\\prd-app-a01\d$\BuildTheBank\Logs\ImportClientDisbursements.log",
        r"\\prd-app-a01\d$\BuildTheBank\Logs\CalculateNaturalGasInventory.log",
    ]

    variable = StringVar(topFrame)
    variable.set(BTBprocesses[0])
    ProcessList = OptionMenu(topFrame,variable,*BTBprocesses)
    ProcessList.pack(fill="x", expand=True, in_= topFrame)
    ListBox1 = Listbox(LogSection, width = 150, height = 40)
    Button(topFrame, text = "View Log", command = partial(displayBTBlog, cal.get_date(), variable, ListBox1)).pack(padx=10, pady=10)
    
    
    ListBox1.pack(fill="x", expand=False, in_= LogSection, side=RIGHT)

    
    bottomFrame.pack(side = BOTTOM)
    topFrame.pack()
    root.mainloop()

def main():
    buildBTBgui()
    ptd = datetime.datetime.today()



