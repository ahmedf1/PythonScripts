'''
this file will do the following

1. Open the ML output file
2. Parse whether the logs processed were success or failure
    a) will have to write some logic to handle weekend scenario
        - ex. check if the day of the week is a Monday
        - if yes, get the three most recent rows (Sat, Sun, Mon)
3. Display result in a windows gui application
'''

from tkinter import * 
import os
import datetime
from functools import partial
#import exportStatusToDashboard
import viewLogsDashboard
import statistics



# 1. Open the ML output file

def openML_outputFile():
    with open(r"C:\Users\Farhad Vantage\Desktop\Python Scripts\ML for Logs\output.txt", 'w+') as file:
        data = file.readlines()
    file.close()
    return data

# 2. Extract lines from the file corresponding to the date
#   a) 2 lines for each day, one for PRD and one for QA
#   b) also implement Weekend logic here
#       - if the current date is a Monday, need to get 6 lines (3 * prd) + (3* QA)

def getRecentLinesFromFile(data, isMonday):
    if isMonday:
        statusSinceFriday = data[-6:]
        return statusSinceFriday
    else:
        status = data[-2:]
        return status


# 3. Parse the extracted lines
#   a) will have to deal with isMonday or not here as well

def getStatusFromLines(linesFromFile):
    # dictionaries where the key will be the date in format yyyy-mm-dd
    # value will be status
    prdStatus = {}
    qaStatus = {}
    accuracies = []
    for line in linesFromFile:
        # remove the newline char and split on the tab space
        splitLine = line.rstrip().split('\t')
        # first part is date (index is 0)
        # second part is processName
        # third part is server
        # forth part is status
        # last part is accuracy
        print(splitLine[1])
        date = splitLine[0]
        status = splitLine[5]
        acc = (splitLine[6]).split(':')[1]
        accuracies.append(float(acc))
        if 'PRD' in line:
            prdStatus[date] = status
        else:
            qaStatus[date] = status
    
    #acc = statistics.mean(accuracies)
    return prdStatus, qaStatus#, acc

# 4. Some functions to open the requested files on command

def openQA_EdfDump(topFrame, key, value):
    top = Toplevel()
    ButtonsSection = Frame(top)
    LogSection = Frame(top)
    ButtonsSection.pack(side = TOP)
    LogSection.pack(side = BOTTOM, fill='x', expand = False)
    
    if value == 'Success':
        if key == str(datetime.date.today()): logContents = openLogFile(r"\\qa-app-a01\d$\CE\EDFDump\EDFDump.log")
        else:
            EDFfilePath = r"\\qa-app-a01\d$\CE\EDFDump\EDFDump.log" + "." + key + ".log"
            print(EDFfilePath)
            logContents = openLogFile(EDFfilePath)
            #logContents = openLogFile(r"C:\Users\fahmed\Desktop\ML for Logs\sample dataset\edf\training set\Failed\EDFDump.log.2018-11-19.log")
            
        
        top.title("QA EDFDump Log For " + key)
        LogViewTitle = Label(top, text ="QA EDFDump Log For " + key, relief = RIDGE, font=("Courier",22),width=50, height = 2, padx = 50)
        LogViewTitle.pack(in_= ButtonsSection, side=TOP)

    else:
        if key == str(datetime.date.today()): logContents = openLogFile(r"\\qa-app-a01\d$\CE\EDFDump\EDFDump.log")
        else:
            EDFfilePath = r"\\qa-app-a01\d$\CE\EDFDump\EDFDump.log" + "." + key + ".log"
            print(EDFfilePath)
            logContents = openLogFile(EDFfilePath)
            #logContents = openLogFile(r"C:\Users\fahmed\Desktop\ML for Logs\sample dataset\edf\training set\Failed\EDFDump.log.2018-12-10.log")
        
        
        #top = Toplevel()
        top.title(key + " QA EDFDump Errors")

        #ButtonsSection = Frame(top)
        #LogSection = Frame(top)

        #ButtonsSection.pack(side = TOP)
        #LogSection.pack(side = BOTTOM, fill='x', expand = False)
        
        #errorsFrame = top.frame()
        #errorsFrame.pack(side = TOP)
        ErrorsTitle = Label(top, text =key + "\t QA EDFDump Errors", relief = RIDGE, font=("Courier",22),width=50, height = 2, padx = 50)
        ErrorsTitle.pack(in_= ButtonsSection, side=TOP)

    ListBox1 = Listbox(top, width = 200, height = 40)
        
    Prices1 = Button(top, text = "Encompass Prices", relief = RIDGE, font=("Courier",16), width = 15, height = 2, wraplength = 120, pady =20, command = partial(switchDisplayedLogSection, 'Prices1', logContents, ListBox1))
    HourlyPositions = Button(top, text = "Encompass 5 Day Hourly Positions", relief = RIDGE, font=("Courier",16), width = 15, height = 2, wraplength = 120, pady =20, command = partial(switchDisplayedLogSection, '5Day', logContents, ListBox1))
    ShapedPositions = Button(top, text = "Encompass Shaped Positions", relief = RIDGE, font=("Courier",16), width = 15, height = 2, wraplength = 120, pady =20, command = partial(switchDisplayedLogSection, 'Shaped', logContents, ListBox1))
    Prices2 = Button(top, text = "Encompass Prices (2nd Run)", relief = RIDGE, font=("Courier",16), width = 15, height = 2, wraplength = 120, pady =20, command = partial(switchDisplayedLogSection, 'Prices2', logContents, ListBox1))
    M2M = Button(top, text = "Encompass M2M", relief = RIDGE, font=("Courier",16), width = 15, height = 2, wraplength = 120, pady =20, command = partial(switchDisplayedLogSection, 'M2M', logContents, ListBox1))

    Prices1.pack(in_= ButtonsSection, side=LEFT)
    HourlyPositions.pack(in_= ButtonsSection, side=LEFT)
    ShapedPositions.pack(in_= ButtonsSection, side=LEFT)
    Prices2.pack(in_= ButtonsSection, side=LEFT)
    M2M.pack(in_= ButtonsSection, side=LEFT)

    ListBox1.pack(fill="x", expand=False, in_= LogSection, side=RIGHT)        
    top.mainloop()
   

def openPRD_EdfDump(topFrame, key, value):
    top = Toplevel()
    ButtonsSection = Frame(top)
    LogSection = Frame(top)
    ButtonsSection.pack(side = TOP)
    LogSection.pack(side = BOTTOM, fill='x', expand = False)
    
    if value == 'Success':
        if key == str(datetime.date.today()): logContents = openLogFile(r"\\prd-app-a01\d$\CE\EDFDump\EDFDump.log")
        else:
            EDFfilePath = r"\\prd-app-a01\d$\CE\EDFDump\EDFDump.log" + "." + key + ".log"
            print(EDFfilePath)
            logContents = openLogFile(EDFfilePath)
            #logContents = openLogFile(r"C:\Users\fahmed\Desktop\ML for Logs\sample dataset\edf\training set\Failed\EDFDump.log.2018-11-19.log")
            
        
        top.title("PRD EDFDump Log For " + key)
        LogViewTitle = Label(top, text ="PRD EDFDump Log For " + key, relief = RIDGE, font=("Courier",22),width=50, height = 2, padx = 50)
        LogViewTitle.pack(in_= ButtonsSection, side=TOP)

    else:
        if key == str(datetime.date.today()): logContents = openLogFile(r"\\prd-app-a01\d$\CE\EDFDump\EDFDump.log")
        else:
            EDFfilePath = r"\\prd-app-a01\d$\CE\EDFDump\EDFDump.log" + "." + key + ".log"
            print(EDFfilePath)
            logContents = openLogFile(EDFfilePath)
            #logContents = openLogFile(r"C:\Users\fahmed\Desktop\ML for Logs\sample dataset\edf\training set\Failed\EDFDump.log.2018-11-19.log")
        
        
        top.title(key + " PRD EDFDump Errors")

        ErrorsTitle = Label(top, text =key + "\t PRD EDFDump Errors", relief = RIDGE, font=("Courier",22),width=50, height = 2, padx = 50)
        ErrorsTitle.pack(in_= ButtonsSection, side=TOP)


    # assemble the GUI
    ListBox1 = Listbox(top, width = 200, height = 40)
        
    Prices1 = Button(top, text = "Encompass Prices", relief = RIDGE, font=("Courier",16), width = 15, height = 2, wraplength = 120, pady =20, command = partial(switchDisplayedLogSection, 'Prices1', logContents, ListBox1))
    HourlyPositions = Button(top, text = "Encompass 5 Day Hourly Positions", relief = RIDGE, font=("Courier",16), width = 15, height = 2, wraplength = 120, pady =20, command = partial(switchDisplayedLogSection, '5Day', logContents, ListBox1))
    ShapedPositions = Button(top, text = "Encompass Shaped Positions", relief = RIDGE, font=("Courier",16), width = 15, height = 2, wraplength = 120, pady =20, command = partial(switchDisplayedLogSection, 'Shaped', logContents, ListBox1))
    Prices2 = Button(top, text = "Encompass Prices (2nd Run)", relief = RIDGE, font=("Courier",16), width = 15, height = 2, wraplength = 120, pady =20, command = partial(switchDisplayedLogSection, 'Prices2', logContents, ListBox1))
    M2M = Button(top, text = "Encompass M2M", relief = RIDGE, font=("Courier",16), width = 15, height = 2, wraplength = 120, pady =20, command = partial(switchDisplayedLogSection, 'M2M', logContents, ListBox1))

    Prices1.pack(in_= ButtonsSection, side=LEFT)
    HourlyPositions.pack(in_= ButtonsSection, side=LEFT)
    ShapedPositions.pack(in_= ButtonsSection, side=LEFT)
    Prices2.pack(in_= ButtonsSection, side=LEFT)
    M2M.pack(in_= ButtonsSection, side=LEFT)

    ListBox1.pack(fill="x", expand=False, in_= LogSection, side=RIGHT)        
    top.mainloop()
    

# 5. Function that retrieves entire log 

def openLogFile(filepath):
    with open(filepath, 'r') as file:
        data = file.readlines()
    file.close()
    return data

# 6. Functions for retreiving parts of log

def getEncompassPrices_FirstRun(logContents):
    EncompassPrices_FirstRun = []
    for line in range(0, len(logContents)):
        # this signifies the first Run of Encompass Prices
        if 'EDFPrices' in logContents[line]:
            # keep going until we reach Encompass Prices
            for j in range(line, len(logContents)):
                if 'Encompass Prices' in logContents[j]:
                    EncompassPrices_FirstRun.append(logContents[j-1])
                    index = j
                    while ('Finished EDFPrices' not in logContents[index]):
                        EncompassPrices_FirstRun.append(logContents[index])
                        index += 1
                    EncompassPrices_FirstRun.append(logContents[index])
                    EncompassPrices_FirstRun.append(logContents[index+1])
                    return EncompassPrices_FirstRun

def getEncompassHourlyPositions(logContents):
    EncompassHourlyPositions = []
    for i in range(0, len(logContents)):
        if 'Hourly Positions *' in logContents[i]:
            EncompassHourlyPositions.append(logContents[i-1])
            index = i
            while ('RunShapedPositions' not in logContents[index]):
                EncompassHourlyPositions.append(logContents[index])
                index += 1
            return EncompassHourlyPositions

def getEncompassShapedPositions(logContents):
    EncompassShapedPositions = []
    for i in range(0, len(logContents)):
        if 'Shaped Positions *' in logContents[i]:
            EncompassShapedPositions.append(logContents[i-1])
            index = i
            while ('RunPrices' not in logContents[index]):
                EncompassShapedPositions.append(logContents[index])
                index += 1
            return EncompassShapedPositions

def getEncompassPrices_SecondRun(logContents):
    EncompassPrices_SecondRun = []
    for line in range(0, len(logContents)):
        # this signifies the second Run of Encompass Prices, this will be after 5:30AM
        if 'Encompass Prices' in logContents[line] and '06:3' in logContents[line]:
            EncompassPrices_SecondRun.append(logContents[line-1])
            lineIterator = line
            while ('RunM2MEdf' not in logContents[lineIterator]):
                EncompassPrices_SecondRun.append(logContents[lineIterator])
                lineIterator += 1
            return EncompassPrices_SecondRun
            
def getEncompassM2M(logContents):
    EncompassM2M = []
    for i in range(0, len(logContents)):
        if 'Encompass M2M *' in logContents[i]:
            EncompassM2M.append(logContents[i-1])
            index = i
            while ('Finished EDFDump' not in logContents[index]):
                EncompassM2M.append(logContents[index])
                index += 1
            EncompassM2M.append(logContents[index])
            EncompassM2M.append(logContents[index+1])
            return EncompassM2M

# 7. Function for switching displayed log section, triggered by button click

def switchDisplayedLogSection(sectionToDisplay, logContents, ListBoxObject):
    # first remove anything currently in the list box
    ListBoxObject.delete(0,END)
    if(sectionToDisplay == 'Prices1'): logToDisplay = getEncompassPrices_FirstRun(logContents)
    elif(sectionToDisplay == '5Day'): logToDisplay = getEncompassHourlyPositions(logContents)
    elif(sectionToDisplay == 'Shaped'): logToDisplay = getEncompassShapedPositions(logContents)
    elif(sectionToDisplay == 'Prices2'): logToDisplay = getEncompassPrices_SecondRun(logContents)
    elif(sectionToDisplay == 'M2M'): logToDisplay = getEncompassM2M(logContents)

    index = 0   
    for line in logToDisplay:
        ListBoxObject.insert(index,line)
        if sectionToDisplay == '5Day' and (index == 3) and len(logToDisplay) == 4:
            index += 1
            ListBoxObject.insert(index, "[mmm dd 05:30:01 A -05:00] INFO  EDFDump RunPositions(0) - Success\n")
            ListBoxObject.itemconfig(index, bg='light green')
        if 'ERROR' in line:
            ListBoxObject.itemconfig(index, bg='pink')
        if 'Success' in line:
            ListBoxObject.itemconfig(index, bg='light green')
        index += 1
    


# 8. Build GUI

def buildGui(prdStatus, qaStatus):
    root = Tk()
    root.resizable(width=False, height=False)
    topFrame = Frame(root)
    bottomFrame = Frame(root)
    bottomFrame.pack(side = BOTTOM)
    processName = Label(topFrame, text ='EDFDump', relief = RIDGE, font=("Courier",22), width=30)
    #Accuracy = Label(topFrame, text =str(acc) , relief = RIDGE, font=("Courier",22), width=30, bg = ('light green' if acc > 0.7 else 'pink'),)
    #Accuracy.pack(fill="x", expand=True, in_= topFrame)
    processName.pack(fill="x", expand=True, in_= topFrame)
    topFrame.pack()
    # 3 rows (Date, serverName, status)
    # 2 columns (Prd, QA)
    
    counterForColumnIncrement = 0
    for key in prdStatus:
        Label(bottomFrame, text =key, relief = RIDGE, font=("Courier",22), width = 15, height = 2).grid(row = 0, column=counterForColumnIncrement)
        Label(bottomFrame, text ="PRD", relief = RIDGE, font=("Courier",22), width = 15, height = 2).grid(row = 1, column=counterForColumnIncrement)
        Label(bottomFrame, text =prdStatus[key], relief = RIDGE, font=("Courier",22), bg = ('light green' if prdStatus[key] == 'Success' else 'pink'), width = 15, height = 3).grid(row = 2, column=counterForColumnIncrement)  

        openlogPRD = partial(openPRD_EdfDump, topFrame, key, prdStatus[key])
        #insertPRDSuccessintoDashboard = partial(exportStatusToDashboard.main, 'Success', "", key, 1)
        #insertPRDSmallIssueintoDashboard = partial(exportStatusToDashboard.main, 'Small Issue', "", key, 1)
        
        Button(bottomFrame, text = ("View Log" if prdStatus[key] == 'Success' else 'View Errors'), relief = RIDGE, font=("Courier",22), width = 15, height = 2,command = openlogPRD).grid(row = 3, column=counterForColumnIncrement)
        #Button(bottomFrame, text = "Insert Success into Dashboard", relief = RIDGE, font=("Courier",22), width = 15, height = 4, wraplength=160, command=insertPRDSuccessintoDashboard).grid(row = 4, column=counterForColumnIncrement)
        #Button(bottomFrame, text = "Insert Issue into Dashboard", relief = RIDGE, font=("Courier",22), width = 15, height = 4, wraplength=160, command=insertPRDSmallIssueintoDashboard).grid(row = 5, column=counterForColumnIncrement)
        counterForColumnIncrement += 1
        
    for key in qaStatus:
        Label(bottomFrame, text =key, relief = RIDGE, font=("Courier",22), width = 15, height = 2).grid(row = 0, column=counterForColumnIncrement)
        Label(bottomFrame, text ="QA", relief = RIDGE, font=("Courier",22), width = 15, height = 2).grid(row = 1, column=counterForColumnIncrement)
        Label(bottomFrame, text =qaStatus[key], relief = RIDGE, font=("Courier",22), bg = ('light green' if qaStatus[key] == 'Success' else 'pink'), width = 15, height = 3).grid(row = 2, column=counterForColumnIncrement)

        openlogQA = partial(openQA_EdfDump,topFrame, key, qaStatus[key])
        #insertQASuccessintoDashboard = partial(exportStatusToDashboard.main, "", "Success", key, 1)
        #insertQASmallIssueintoDashboard = partial(exportStatusToDashboard.main, "", "Small Issue", key, 1)
        
        Button(bottomFrame, text = ("View Log" if qaStatus[key] == 'Success' else 'View Errors'), relief = RIDGE, font=("Courier",22), width = 15, height = 2,command = openlogQA ).grid(row = 3, column=counterForColumnIncrement)
        #Button(bottomFrame, text = "Insert Success into Dashboard", relief = RIDGE, font=("Courier",22), width = 15, height = 4, wraplength=160, command=insertQASuccessintoDashboard).grid(row = 4, column=counterForColumnIncrement)
        #Button(bottomFrame, text = "Insert Issue into Dashboard", relief = RIDGE, font=("Courier",22), width = 15, height = 4, wraplength=160, command=insertQASmallIssueintoDashboard).grid(row = 5, column=counterForColumnIncrement)
        counterForColumnIncrement += 1

    bottomFrame.pack(fill="x", expand=True, side = BOTTOM)
    root.mainloop()


def main():
    isMonday =(datetime.datetime.today().weekday() == 0)
    EntirefileContents = openML_outputFile()
    linesFromPreviousDay = getRecentLinesFromFile(EntirefileContents, isMonday)
    print(linesFromPreviousDay)
    prdStatus, qaStatus = getStatusFromLines(linesFromPreviousDay)
    buildGui(prdStatus,qaStatus)
    # added the input() so that when this script is run by the task scheduler
    # the window will stay open instead of closing on completion



