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
    logContents = getContentsForView('PRD', r"\\prd-app-a01\d$\CE\RepCalcs\RepCalcs.log")
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
config.read(r"\\qa-app-a01\d$\CE\Repcalcs\RepCalcs.ini")
repId = config.get("Process Routine Configuration","recRepId")
## next rerun with replacing the repId for each failed client



def runFailedRecv():
    for rerunclient in failedClients:
        config.set("Process Routine Configuration","recRepId",str(rerunclient))
        config.set("Process Routine Configuration","importreceivables","true")
        print(config.get("Process Routine Configuration","recRepId"))
        with open(r"\\qa-app-a01\d$\CE\Repcalcs\RepCalcs.ini", "w") as f:
            config.write(f)

        cmd = r"\\qa-app-a01\d$\CE\MasterConsole.exe " + """--PRocessname="REPSXDLOAD" --importScheduledLoad="true" """
        subprocess.call(cmd)
        
     
    config.set("Process Routine Configuration","recRepId","0")
    config.set("Process Routine Configuration","importreceivables","false")
    with open(r"\\qa-app-a01\d$\CE\Repcalcs\RepCalcs.ini", "w") as f:
            config.write(f)
    print("Finished Rerun for error client!")
    
    #print(config.get("Process Routine Configuration","recRepId"))


# \\qa-app-a01\d$\CE\MasterConsole.exe
# --PRocessname="REPSXDLOAD" --importScheduledLoad="true"

#runFailedRecv()

cmd = r"\\qa-app-a01\d$\CE\MasterConsole.exe " + """--PRocessname="REPSXDLOAD" --importScheduledLoad="true" """
subprocess.call(cmd)
