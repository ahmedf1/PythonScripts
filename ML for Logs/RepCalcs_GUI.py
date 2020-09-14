'''
    This script will parse out individual client sections from the RepCalcs log
    and display them in a manner similar to the way the sections from EDFDump
    are displayed

    This script will run in the morning, therefore processing only the contracts
    process within RepCalcs.
    Can do a separate script to parse out Receivables at the end of the day or
    just add to this, have two options Contracts vs Receivables (RepSxdLoad)

    also add DB support so that it just queries the database to get names of
    active clients in order to stay up to date without any manual updates

    Errors to be reported include:
    - Missing files
    - invalid chars in file leading to program failure
    - etc.

'''
from tkinter import *
import tkinter as tk
import glob
import os
import datetime
from functools import partial
import exportStatusToDashboard
import viewLogsDashboard
import statistics

def openLogFile(filepath):
    with open(filepath, 'r') as file:
        data = file.readlines()
    file.close()
    return data

def parseClientsContractsFromRepCalcsLog(logContents, isMonday, isPRD):
    # if it's monday, then contracts are skipped since yesterday was not a business day, and we have no client contracts to parse out
    if isMonday and isPRD:
        return logContents
    else:
        #print(logContents)
        ClientContractSections = {}
        # separate the log based on client sections
        for line in range(0, len(logContents)):
            ContractSectionOfLog = []
            if 'Download Contracts for' in logContents[line]:
                # keep going til we reach the end of the section for this client
                splitLine = logContents[line].split('for ')
                client, mailboxInfo = splitLine[1].split('(')
                for j in range(line, len(logContents)):
                    ContractSectionOfLog.append(logContents[j-1])
                    ContractSectionOfLog.append(logContents[j])
                    ContractSectionOfLog.append(logContents[j+1])
                    index = j + 2
                    while '*********************' not in logContents[index] :#('Skipping cleanup' not in logContents[index]):
                        ContractSectionOfLog.append(logContents[index])
                        index += 1
                    ClientContractSections[client] = ContractSectionOfLog
                    break
        return ClientContractSections

def parseClientsRecvFromRepCalcsLog(logContents):
    ClientRecvSections = {}
    # separate the log based on client sections
    for line in range(0, len(logContents)):
        RecvSectionOfLog = []
        if 'Download Receivables for' in logContents[line]:
            # keep going til we reach the end of the section for this client
            splitLine = logContents[line].split('for ')
            client, mailboxInfo = splitLine[1].split('(')
            #print(client)
            for j in range(line, len(logContents)):
                RecvSectionOfLog.append(logContents[j-1])
                RecvSectionOfLog.append(logContents[j])
                RecvSectionOfLog.append(logContents[j+1])
                index = j + 2
                try:
                    while "+++++++++++++++++++++++++++++++++++++++++++++++++++++++" not in logContents[index] and 'Finished RepSxdLoad' not in logContents[index]:#('Skipping cleanup' not in logContents[index]):
                        try:
                            RecvSectionOfLog.append(logContents[index])
                            index += 1
                        except:
                            RecvSectionOfLog.append("PROCESS IS STILL RUNNNING")
                            break
                    #print(RecvSectionOfLog)
                    ClientRecvSections[client] = RecvSectionOfLog
                    break
                except:
                    RecvSectionOfLog.append("PROCESS IS STILL RUNNNING")
                    break

                break
    return ClientRecvSections

def switchDisplayedContractSection(clientName, ListBoxObject, currentView, currentFilePath,isPRD):
    if clientName == 'ALL':
        logContents = getContentsForView(currentView, currentFilePath)
        clientContractSection = parseClientsContractsFromRepCalcsLog(logContents, True, isPRD)

    else:
        logContents = getContentsForView(currentView, currentFilePath)
        ClientContractsSections = parseClientsContractsFromRepCalcsLog(logContents, False, isPRD)
        clientContractSection = ClientContractsSections[clientName]
    
    ListBoxObject.delete(0,END)
    index = 0
    for line in clientContractSection:
        ListBoxObject.insert(index, '['+ currentView + ']\t' + line)
        if 'ERROR' in line:
            ListBoxObject.itemconfig(index, bg = 'pink')
        if 'new Contracts' in line:
            ListBoxObject.itemconfig(index, bg = 'light green')
        index +=1        

def switchFileList(isPRD, FileListOBJ, currentFilePath):
    FileListOBJ['menu'].delete(0,'end')
    currentFilePath.set('')
    if isPRD:
        FileList = glob.glob(r"\\prd-app-a01\d$\CE\RepCalcs\RepCalcs.log*")
        for filepath in FileList:
            FileListOBJ['menu'].add_command(label=filepath, command = tk._setit(currentFilePath, filepath))
    else:
        FileList = glob.glob(r"\\qa-app-a01\d$\CE\RepCalcs\RepCalcs.log*")
        for filepath in FileList:
            FileListOBJ['menu'].add_command(label=filepath, command = tk._setit(currentFilePath, filepath))

    currentFilePath.set(FileList[0]) # 
        
        


def displayContracts(switchBTWN_QA_PRD,ListBox1, isMonday, bottomFrame, CurrentView, currentFilePath, FileList):
    for widget in bottomFrame.winfo_children():
        widget.destroy()
    isprd = True
    if switchBTWN_QA_PRD['text'] == 'Switch to QA':
        switchBTWN_QA_PRD.configure(text='Switch to PRD')
        isprd = False
        CurrentView.configure(text="Currently Viewing QA")

    elif switchBTWN_QA_PRD['text'] == 'Switch to PRD':
        switchBTWN_QA_PRD.configure(text='Switch to QA')
        CurrentView.configure(text="Currently Viewing PRD")

    text = 'PRD' if isprd else 'QA'
    switchFileList(isprd, FileList, currentFilePath)
        #switchBTWN_QA_PRD['text']
    logContents = getContentsForView(text, currentFilePath)#switchBTWN_QA_PRD['text'])
    ClientContractsSections = parseClientsContractsFromRepCalcsLog(logContents, isMonday, isprd)
    if isMonday and isprd:
        switchDisplayedContractSection('ALL', ListBox1, text, currentFilePath, isprd)
        Button(bottomFrame, text = "View Log", relief = RIDGE, font=("Courier",15), width = 15, height = 2, command = partial(switchDisplayedContractSection, 'ALL', ListBox1,text,currentFilePath,isprd )).pack()#row = 2, column=counterForColumnIncrement)

    else:    
        counterForColumnIncrement = 0
        for key in ClientContractsSections:
            Label(bottomFrame, text =key, relief = RIDGE, font=("Courier",15), width = 15, height = 2).grid(row = 0, column=counterForColumnIncrement) 
            Button(bottomFrame, text = "View Log", relief = RIDGE, font=("Courier",15), width = 15, height = 2, command = partial(switchDisplayedContractSection, key, ListBox1,text,currentFilePath,isprd )).grid(row = 2, column=counterForColumnIncrement)
            counterForColumnIncrement += 1
        

def getContentsForView(currentView,currentFilePath):
    if currentView == 'PRD':
        logContents = openLogFile(currentFilePath.get())
        #logContents = openLogFile(r"\\prd-app-a01\d$\CE\RepCalcs\RepCalcs.log")
    else:# currentView == 'QA':
        logContents = openLogFile(currentFilePath.get())
        #logContents = openLogFile(r"\\qa-app-a01\d$\CE\RepCalcs\RepCalcs.log")
    return logContents


def displayReceivables(switchBTWN_QA_PRD,ListBox1, bottomFrame, CurrentView,currentFilePath,FileList):
    for widget in bottomFrame.winfo_children():
        widget.destroy()
    isprd = True
    if switchBTWN_QA_PRD['text'] == 'Switch to QA':
        switchBTWN_QA_PRD.configure(text='Switch to PRD')
        isprd = False
        CurrentView.configure(text="Currently Viewing QA")

    elif switchBTWN_QA_PRD['text'] == 'Switch to PRD':
        switchBTWN_QA_PRD.configure(text='Switch to QA')
        CurrentView.configure(text="Currently Viewing PRD")

    text = 'PRD' if isprd else 'QA'
    switchFileList(isprd, FileList, currentFilePath)
        #switchBTWN_QA_PRD['text']
    logContents = getContentsForView(text, currentFilePath)#switchBTWN_QA_PRD['text'])
    ClientRecvSections = parseClientsRecvFromRepCalcsLog(logContents)
    
    counterForColumnIncrement = 0
    for key in ClientRecvSections:
        Label(bottomFrame, text =key, relief = RIDGE, font=("Courier",15), width = 15, height = 2).grid(row = 0, column=counterForColumnIncrement) 
        Button(bottomFrame, text = "View Log", relief = RIDGE, font=("Courier",15), width = 15, height = 2, command = partial(switchDisplayedRECVsection, key, ListBox1,text,currentFilePath )).grid(row = 2, column=counterForColumnIncrement)
        counterForColumnIncrement += 1

def switchDisplayedRECVsection(clientName, ListBoxOBJ, currentView, currentFilePath):
    logContents = getContentsForView(currentView, currentFilePath)
    ClientRecvSections = parseClientsRecvFromRepCalcsLog(logContents)
    currentRecvSection = ClientRecvSections[clientName]
    #print(currentRecvSection)
    
    ListBoxOBJ.delete(0,END)
    index = 0
    for line in currentRecvSection:
        ListBoxOBJ.insert(index, '['+ currentView + ']\t' + line)
        if 'ERROR' in line:
            ListBoxOBJ.itemconfig(index, bg = 'pink')
        if 'Rows count' in line:
            ListBoxOBJ.itemconfig(index, bg = 'light green')
        index +=1

def getClientRECV(processName, switchBTWN_QA_PRD, ViewRecvBttn, ListBox1, isMonday, bottomFrame, CurrentView, variable, FileList):
    if processName['text'] == "RepCalcs Receivables":
        processName.configure(text='RepCalcs Contracts')
        ViewRecvBttn.configure(text='Click to View Receivables')
        switchBTWN_QA_PRD.configure(command = partial(displayContracts, switchBTWN_QA_PRD,ListBox1,isMonday, bottomFrame, CurrentView,variable,FileList))
    else:
        processName.configure(text='RepCalcs Receivables')
        ViewRecvBttn.configure(text='Click to View Contracts')
        switchBTWN_QA_PRD.configure(command = partial(displayReceivables,switchBTWN_QA_PRD,ListBox1, bottomFrame, CurrentView,variable,FileList))
    switchBTWN_QA_PRD.invoke()
    
def buildGui(isMonday):
    root = Tk()
    root.resizable(width=False, height=False)
    topFrame = Frame(root)
    bottomFrame = Frame(root)
    ContractSection = Frame(root)
    ContractSection.pack(side = BOTTOM, fill='x', expand = False)
    bottomFrame.pack(side = BOTTOM)
    processName = Label(topFrame, text ='RepCalcs Contracts', relief = RIDGE, font=("Courier",22), width=30)
    ViewRecv = Button(topFrame, text ='Click to View Receivables', relief = RIDGE, font=("Courier",22), width=30, state=(DISABLED if datetime.datetime.now().hour < 11 else ACTIVE))

    PRDfiles = glob.glob(r"\\prd-app-a01\d$\CE\RepCalcs\RepCalcs.log*")
    QAfiles = glob.glob(r"\\qa-app-a01\d$\CE\RepCalcs\RepCalcs.log*")
    variable = StringVar(topFrame)
    variable.set(PRDfiles[0]) # 

    

    FileList = OptionMenu(topFrame, variable, *PRDfiles)
   #PTDdateTime = Label(topFrame, text =str(datetime.date.today()), relief = RIDGE, font=("Courier",22), width=30)



    ViewRecv.pack(fill="y", expand=True, in_= topFrame, side = RIGHT)
    processName.pack(fill="x", expand=True, in_= topFrame)
    FileList.pack(fill="x", expand=True, in_= topFrame)

    ListBox1 = Listbox(root, width = 255, height = 40)

    #currentView = StringVar()
    #currentView.set("PRD")
    switchBTWN_QA_PRD  = Button(topFrame, relief = RIDGE, font=("Courier",15), width = 15, height = 2)
    CurrentView = Label(topFrame, relief = RIDGE, font=("Courier",15), width = 15, height = 2)
    CurrentView.configure(text = 'Currently Viewing QA')
    switchBTWN_QA_PRD.configure(text='Switch to PRD')
    switchBTWN_QA_PRD.configure(command = partial(displayContracts, switchBTWN_QA_PRD,ListBox1,isMonday, bottomFrame, CurrentView,variable,FileList))
    switchBTWN_QA_PRD.invoke()
    CurrentView.pack(fill="x", expand=True, in_= topFrame)
    switchBTWN_QA_PRD.pack(fill="x", expand=True, in_= topFrame)

    ViewRecv.configure(command = partial(getClientRECV, processName, switchBTWN_QA_PRD, ViewRecv,ListBox1, isMonday, bottomFrame, CurrentView,variable,FileList))
    
    
    topFrame.pack()
    '''
    logContents = getContentsForView(switchBTWN_QA_PRD['text'])
    ClientContractsSections = parseClientsFromRepCalcsLog(logContents, isMonday)
    
   

    
    

    if isMonday:
        switchDisplayedContractSection('ALL', ClientContractsSections, ListBox1)

    else:    
        counterForColumnIncrement = 0
        for key in ClientContractsSections:
            Label(bottomFrame, text =key, relief = RIDGE, font=("Courier",15), width = 15, height = 2).grid(row = 0, column=counterForColumnIncrement) 
            Button(bottomFrame, text = "View Log", relief = RIDGE, font=("Courier",15), width = 15, height = 2, command = partial(switchDisplayedContractSection, key, ClientContractsSections[key], ListBox1, switchBTWN_QA_PRD['text'])).grid(row = 2, column=counterForColumnIncrement)
            counterForColumnIncrement += 1

    '''          
    ListBox1.pack(fill="x", expand=False, in_= ContractSection, side=RIGHT)
  

def main():
    isMonday = (datetime.datetime.today().weekday() == 0)
    buildGui(isMonday)


