import windows_task_scheduler as wts

#wts.run_task(task_name='RepSxdLoad')



'''
1. open log/get run results from RepSxdLoad
2. run RepSxdLoad by changing the config file for specfic repIds
3. always set repId to 0 at the end (reset for tomorrow's run)

'''
from  configparser import *
import subprocess

# first try with log file

def openLogFile(filepath):
    with open(filepath, 'r') as file:
        data = file.readlines()
    file.close()
    return data

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

def getContentsForView(currentView,currentFilePath):
    if currentView == 'PRD':
        logContents = openLogFile(currentFilePath)
        #logContents = openLogFile(r"\\prd-app-a01\d$\CE\RepCalcs\RepCalcs.log")
    else:# currentView == 'QA':
        logContents = openLogFile(currentFilePath)
        #logContents = openLogFile(r"\\qa-app-a01\d$\CE\RepCalcs\RepCalcs.log")
    return logContents

clients = ['Volt ','Discount ','GB Power ','APG ']
clientsRepId = {'Volt ': [85, False, False], 'Discount ': [46,False, False], 'GB Power ': [41, False,False], 'APG ': [6, False,False] }

def openRecvLog():
    logContents = getContentsForView('PRD', r"D:\CE\Repcalcs\RepCalcs.log")
    ClientRecvSections = parseClientsRecvFromRepCalcsLog(logContents)
    for client in clients:
        currentRecvSection = ClientRecvSections[client]
        index = 1
        for line in currentRecvSection:
            if 'Rows count' in line:
                clientsRepId[client][index] = True
                index+=1
            if 'ERROR' in line:
                clientsRepId[client][index] = False
                index+=1
            if index > 2:
                break
            


## next add the result to dicionary
## change config file to hold missing recv
# loop thru missing list and rerun then rerun the RepSxDLoad

def getFailedRecv():
    clientsToRerun = []
    for client in clientsRepId:
        repId = clientsRepId[client][0]
        if False in clientsRepId[client]:
            print("need to rerun client: ", repId)
            clientsToRerun.append(repId)
    return clientsToRerun
        
    
openRecvLog()
failedClients = getFailedRecv()

config = ConfigParser(allow_no_value=True)
config.read(r"D:\CE\Repcalcs\RepCalcs.ini")
repId = config.get("Process Routine Configuration","recRepId")
## next rerun with replacing the repId for each failed client

import sys

sys.path.extend(('C:\\Users\\fahmed\\AppData\\Local\\Programs\\Python\\Python35\\Lib\\site-packages\\win32', 'C:\\Users\\fahmed\\AppData\\Local\\Programs\\Python\\Python35\\Lib\\site-packages\\win32\\lib', 'C:\\Users\\fahmed\\AppData\\Local\\Programs\\Python\\Python35\\Lib\\site-packages\\Pythonwin'))

import win32com.client

TASK_ENUM_HIDDEN = 1
TASK_STATE = {0: 'Unknown',
              1: 'Disabled',
              2: 'Queued',
              3: 'Ready',
              4: 'Running'}

def getTaskStatus():
    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()

    n = 0
    folders = [scheduler.GetFolder('\\')]
    while folders:
        folder = folders.pop(0)
        folders += list(folder.GetFolders(0))
        tasks = list(folder.GetTasks(TASK_ENUM_HIDDEN))
        n += len(tasks)
        for task in tasks:
            if task.Path == r'\RepSxdLoad':
                settings = task.Definition.Settings
                print('Path       : %s' % task.Path)
                print('Hidden     : %s' % settings.Hidden)
                print('State      : %s' % TASK_STATE[task.State])
                print('Last Run   : %s' % task.LastRunTime)
                print('Last Result: %s\n' % task.LastTaskResult)
                while TASK_STATE[task.State] == 'Running':
                    print("Running")
                print("ran")
        
    print('Listed %d tasks.' % n)


def runFailedRecv():
    for rerunclient in failedClients:
        config.set("Process Routine Configuration","recRepId",str(rerunclient))
        #config.set("Process Routine Configuration","importreceivables","true")
        print(config.get("Process Routine Configuration","recRepId"))
        with open(r"D:\CE\Repcalcs\RepCalcs.ini", "w") as f:
            config.write(f)

        wts.run_task(task_name='RepSxdLoad')
        getTaskStatus()
        
        
        
    config.set("Process Routine Configuration","recRepId","0")
    config.set("Process Routine Configuration","importreceivables","false")
    with open(r"D:\CE\Repcalcs\RepCalcs.ini", "w") as f:
            config.write(f)
    print("Finished Rerun for error client!")
    
    #print(config.get("Process Routine Configuration","recRepId"))


# \\qa-app-a01\d$\CE\MasterConsole.exe
# --PRocessname="REPSXDLOAD" --importScheduledLoad="true"

runFailedRecv()

