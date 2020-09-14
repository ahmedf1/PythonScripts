# this script will check the prd-app-a01 server in the BuildTheBank directory
# to ensure that the BAI file was transferred succesfully via the Secure Client
# app

import os
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import datetime
from datetime import timedelta
import glob
import retreivingActiveClients

import sys
# need to do this in order to access modules in a different directory
sys.path.insert(0, r'C:\Users\fahmed\Desktop\ML for Logs')
from EDFDump_GUI import *
from RepCalcs_GUI import *

def isMonday():
    #this function just checks if today is a Monday since there is special behavior on Mondays
    dayOfWeek = datetime.datetime.today().weekday()
    return dayOfWeek == 0

def getDateSaturday():
    d = datetime.datetime.today() - timedelta(days=2)
    return d

def getDateSunday():
    d = datetime.datetime.today() - timedelta(days=1)
    return d

def checkForRepCalcsSuccess():
    #check if its monday
    isNotMonday = datetime.datetime.today().weekday()   # Monday is represented as 0 (false in boolean)
    logContents = openLogFile(r"\\prd-app-a01\d$\CE\RepCalcs\RepCalcs.log")

    # since the only clients that upload their contract files to us are GBPower and APG
    # can just create the txt file for solely these clients and report their statuses

    emailBodyReport = ''
    html = """\
        <tr>
                <th style="background-color: #ffffff;">RepCalcs Contracts Client</th>
                <th style="background-color: #ffffff;">Status</th>
        </tr>
    """

    if isNotMonday:
        ClientContractSections = parseClientsContractsFromRepCalcsLog(logContents,False,True)
        for key in ClientContractSections:
            if key == 'GB Power ':
                with open(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\GBPowerContracts.txt', 'w+') as fileToWrite:
                    for line in ClientContractSections[key]:
                        if '** Inserted ' in line:
                            lineToCheck = line.split()
                            numInserted = int(lineToCheck[10])
                            if(numInserted > 0): success = True
                        fileToWrite.write(line)

                if success == True:
                    emailBodyReport += "GB Power Contracts Status..................SUCCESS\n"
                    html += "<tr><td>GB Power</td><td style = 'text-align:center;'>&#9989;</td></tr>"
                else:
                    emailBodyReport += "GB Power Contracts Status..................FAILED\n"
                    html += "<tr><td>GB Power</td><td style = 'text-align:center;'>FAILED</td></tr>"

            if key == 'APG ':
                with open(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\APGContracts.txt', 'w+') as fileToWrite:
                    for line in ClientContractSections[key]:
                        if '** Inserted ' in line:
                            lineToCheck = line.split()
                            numInserted = int(lineToCheck[10])
                            if(numInserted > 0): success = True
                        fileToWrite.write(line)

                if success == True:
                    emailBodyReport += "APG Contracts Status..................SUCCESS\n"
                    html += "<tr><td>APG</td><td style = 'text-align:center;'>&#9989;</td></tr>"
                else:
                    emailBodyReport += "APG Contracts Status..................FAILED\n"
                    html += "<tr><td>APG</td><td style = 'text-align:center;'>FAILED</td></tr>"
                
    else:
        emailBodyReport += "Today is Monday, there are no Contracts processed on Mondays, see File attached for status!\n"

        errors = False
        with open(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\MondayRepContract.txt', 'w+') as fileToWrite:
            for line in logContents:
                if "~~ Finished RepCalcs ~" not in line:
                    fileToWrite.write(line)
                elif "ERROR" in line:
                    errors = True
                    fileToWrite.write(line)
                else:
                    fileToWrite.write(line)
                    break
        if not errors:
            html += "<tr><td>PTD is MONDAY</td><td style = 'text-align:center;'>&#9989;</td></tr>"
        else:
            html += "<tr><td>PTD is MONDAY</td><td style = 'text-align:center;'>FAILED</td></tr>"
            
        # now need to attach files for Saturday and Sunday
        # saturday is treated like anyother day, and sunday is treated like a monday (no contracts processing)
        dateSaturday = str(getDateSaturday()).split('-')
        dateSunday = str(getDateSunday()).split('-')

        keySun = dateSunday[0] + '-' + dateSunday[1] + '-' + dateSunday[2][:2]
        RepCalcsfilepathSun = r"\\prd-app-a01\d$\CE\RepCalcs\RepCalcs.log" + "." + keySun + ".log"
        logContents = openLogFile(RepCalcsfilepathSun)
        
        emailBodyReport += "\nYesterday was Sunday, there are no Contracts processed on Sunday, see File attached for status!\n"
        errors = False
        with open(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\SundayRepContract.txt', 'w+') as fileToWrite:
            for line in logContents:
                if "~~ Finished RepCalcs ~" not in line:
                    fileToWrite.write(line)
                elif "ERROR" in line:
                    errors = True
                    fileToWrite.write(line)
                else:
                    fileToWrite.write(line)
                    break
        if not errors:
            html +=  "<tr><td>YESTERDAY PTD is SUNDAY</td><td style = 'text-align:center;'>&#9989;</td></tr>"
        else:
            html += "<tr><td>YESTERDAY PTD is SUNDAY</td><td style = 'text-align:center;'>FAILED</td></tr>"

        keySat = dateSaturday[0] + '-' + dateSaturday[1] + '-' + dateSaturday[2][:2]
        RepCalcsfilepathSat = r"\\prd-app-a01\d$\CE\RepCalcs\RepCalcs.log" + "." + keySat + ".log"
        logContents = openLogFile(RepCalcsfilepathSat)
        emailBodyReport += "\nPTD 2 days ago was Saturday, Showing Contracts Status for Saturday:\n"
        
        html += "<th>PTD 2 DAYS AGO is SATURDAY</th>"

        ClientContractSections = parseClientsContractsFromRepCalcsLog(logContents,False,True)
        with open(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\SaturdayRepContract.txt', 'w+') as fileToWrite:
            for key in ClientContractSections:
                if key == 'GB Power ':
                    for line in ClientContractSections[key]:
                        if '** Inserted ' in line:
                            lineToCheck = line.split()
                            numInserted = int(lineToCheck[10])
                            if(numInserted > 0): success = True
                        fileToWrite.write(line)

                    if success == True:
                        emailBodyReport += "\tGB Power SATURDAY Contracts Status..................SUCCESS\n"
                        html += "<tr><td>GB Power</td><td style = 'text-align:center;'>&#9989;</td></tr>"
                    else:
                        emailBodyReport += "\tGB Power SATURDAY Contracts Status..................FAILED\n"
                        html += "<tr><td>GB Power</td><td style = 'text-align:center;'>FAILED</td></tr>"

                if key == 'APG ':
                    for line in ClientContractSections[key]:
                        if '** Inserted ' in line:
                            lineToCheck = line.split()
                            numInserted = int(lineToCheck[10])
                            if(numInserted > 0): success = True
                        fileToWrite.write(line)

                    if success == True:
                        emailBodyReport += "\tAPG SATURDAY Contracts Status..................SUCCESS\n"
                        html += "<tr><td>APG</td><td style = 'text-align:center;'>&#9989;</td></tr>"
                    else:
                        emailBodyReport += "\tAPG SATURDAY Contracts Status..................FAILED\n"
                        html += "<tr><td>APG</td><td style = 'text-align:center;'>FAILED</td></tr>"

    return emailBodyReport, html


    
    
    
        

def checkForEDFDumpSuccess():
    logContents = openLogFile(r"\\prd-app-a01\d$\CE\EDFDump\EDFDump.log")
    pricesRun1 = getEncompassPrices_FirstRun(logContents)
    hourlyPos = getEncompassHourlyPositions(logContents)
    shapedPos = getEncompassShapedPositions(logContents)
    pricesRun2 = getEncompassPrices_SecondRun(logContents)
    m2m = getEncompassM2M(logContents)

    # first delete all the files contents from the previous day
    if os.path.exists(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\pricesRun1.txt'):
                os.remove(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\pricesRun1.txt') #this deletes the file

    if os.path.exists(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\hourlyPos.txt'):
                os.remove(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\hourlyPos.txt') #this deletes the file

    if os.path.exists(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\shapedPos.txt'):
                os.remove(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\shapedPos.txt') #this deletes the file

    if os.path.exists(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\pricesRun2.txt'):
                os.remove(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\pricesRun2.txt') #this deletes the file

    if os.path.exists(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\m2m.txt'):
                os.remove(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\m2m.txt') #this deletes the file

    emailBodyReport = ''
    html = """\
        <tr>
                <th style="background-color: #ffffff;">Encompass Section</th>
                <th style="background-color: #ffffff;">Status</th>
        </tr>
    """
    
    
    with open(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\pricesRun1.txt', 'w') as fileToWrite:
        success = False
        for line in pricesRun1:
            fileToWrite.write(line)
            if 'Success' in line:
                success = True
    if success:       
        emailBodyReport += "Prices Run #1 Status..................SUCCESS\n"
        html += "<tr><td>Prices Run #1</td><td style = 'text-align:center;'>&#9989;</td></tr>"
    else:
        emailBodyReport += "Prices Run #1 Status..................FAILED\n"
        html += "<tr><td>Prices Run #1</th><td>FAILED</td></tr>"

    with open(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\hourlyPos.txt', 'w') as fileToWrite:
        success = False
        for line in hourlyPos:
            fileToWrite.write(line)
            if 'Success' in line:
                success = True
            elif 'Skipping 5 day positions since its nowhere near the end of the month' in line:
                success = True          
    if success:       
        emailBodyReport += "Hourly Positions Status...............SUCCESS\n"
        html += "<tr><td>Hourly Positions</td><td style = 'text-align:center;'>&#9989;</td></tr>"
    else:
        emailBodyReport += "Hourly Positions Status...............FAILED\n"
        html += "<tr><td>Hourly Positions</td><td>FAILED</td></tr>"
                
            
    with open(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\shapedPos.txt', 'w') as fileToWrite:
        success = False
        for line in shapedPos:
            fileToWrite.write(line)
            if 'Success' in line:
                success = True
    if success:
        emailBodyReport += "Shaped Positions Status.............SUCCESS\n"
        html += "<tr><td>Shaped Positions</td><td style = 'text-align:center;'>&#9989;</td></tr>"
    else:
        emailBodyReport += "Shaped Positions Status.............FAILED\n"
        html += "<tr><td>Shaped Positions</td><td>FAILED</td></tr>"
            
    with open(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\pricesRun2.txt', 'w') as fileToWrite:
        success = False
        for line in pricesRun2:
            fileToWrite.write(line)
            if 'Success' in line:
                success = True
    if success:
        emailBodyReport += "Prices Run #2 Status...................SUCCESS\n"
        html += "<tr><td>Prices Run #2</td><td style = 'text-align:center;'>&#9989;</td></tr>"
    else:
        emailBodyReport += "Prices Run #2 Status...................FAILED\n"
        html += "<tr><td>Prices Run #2</td><td>FAILED</td></tr>"
            
    with open(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\m2m.txt', 'w') as fileToWrite:
        success = False
        for line in m2m:
            fileToWrite.write(line)
            if 'Success' in line:
                success = True
    if success:        
        emailBodyReport += "M2M Status.................................SUCCESS\n"
        html += "<tr><td>M2M Run #2</td><td style = 'text-align:center;'>&#9989;</td></tr>"
    else:
        emailBodyReport += "M2M Status.................................FAILED\n"
        html += "<tr><td>M2M Run #2</td><td>FAILED</td></tr>"
    return emailBodyReport, html
        
        

def checkForBAIfile():
    # first get date for file name matching since the file is
    # distinguishable based on the date
    today = datetime.date.today()
    month = today.strftime("%m")
    year = today.strftime("%y")
    day = today.strftime("%d")

    baiText = "BAI.txt"
    todaysFile = month + day + year + baiText
    html = ''
    list_of_files = glob.glob(r'\\prd-app-a01\d$\BuildTheBank\BaiFiles\*BAI.txt') # * means all if need specific format then *.csv
    latest_file = max(list_of_files, key = os.path.getctime)

    if(todaysFile in latest_file):
        # file is present, it was successfully transferred
        status = "Transfer was successfull, file is present: " + latest_file
        html += '<tr><td>' + latest_file + '</td><td style = "text-align:center;">&#9989;</td></tr>'
    elif(isMonday()):
        status = "Today is Monday, there is no BAI File Uploaded on Mondays!"
        html += '<tr><td>*No BAI File Uploaded on Mondays!*</td><td style = "text-align:center;">&#9989;</td></tr>'
    else:
        status = "Transfer was unsuccessful, check prd-sched-a01 server! \n Latest File is: " + latest_file
        html += '<tr><td>' + latest_file + '</td><td style = "text-align:center;">&#10060;</td></tr>'

    return status, html

def sendEmail(status,emailBodyReportEDF,emailBodyReportRepContract, html):
    fromaddr = "fahmed@vantagecommodities.com"
    toaddr = "fahmed@vantagecommodities.com"
    
   
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 
  
    # storing the senders email address   
    msg['From'] = fromaddr 
  
    # storing the receivers email address  
    msg['To'] = toaddr 
  
    # storing the subject  
    msg['Subject'] = "Daily Logs Status Report"
      
    # string to store the body of the mail
    msg.attach(MIMEText(html, 'html'))
    #msg.attach(MIMEText(htmlEDF, 'html'))

    # attach the body with the msg instance 
    #msg.attach(MIMEText(body, 'plain'))
     
    filenames = [
        r"C:\Users\fahmed\Desktop\Daily Log Reporting Script\pricesRun1.txt"
        , r"C:\Users\fahmed\Desktop\Daily Log Reporting Script\hourlyPos.txt"
        , r"C:\Users\fahmed\Desktop\Daily Log Reporting Script\shapedPos.txt"
        , r"C:\Users\fahmed\Desktop\Daily Log Reporting Script\pricesRun2.txt"
        , r"C:\Users\fahmed\Desktop\Daily Log Reporting Script\m2m.txt"
    ]
    
    if isMonday():
        filenames.append(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\MondayRepContract.txt')
        filenames.append(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\SundayRepContract.txt')
        filenames.append(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\SaturdayRepContract.txt')
    else:
        filenames.append(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\GBPowerContracts.txt')
        filenames.append(r'C:\Users\fahmed\Desktop\Daily Log Reporting Script\APGContracts.txt')

    for filename in filenames:
        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream')

        # To change the payload into encoded form 
        p.set_payload((open(filename, 'rb')).read()) 

        # encode into base64 
        encoders.encode_base64(p) 
   
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 
  
        # attach the instance 'p' to instance 'msg' 
        msg.attach(p)
  
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
  
    # start TLS for security 
    s.starttls() 
  
    # Authentication 
    s.login(fromaddr, "Futplayer23") 
  
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
  
    # sending the mail
    s.sendmail(fromaddr, toaddr, text)
  
    # terminating the session 
    s.quit() 

def main():
    html = '''
    <html>
      <head></head>
      <body>
        <table style="background-color: #dddddd;">
        <tr>
                <th style="background-color: #ffffff;">BAI LATEST FILE</th>
                <th style="background-color: #ffffff;width:50px;">Status</th>
        </tr>
    '''
    status, htmlBAI = checkForBAIfile()  
    emailBodyReportEDF, htmlEDF = checkForEDFDumpSuccess()
    emailBodyReportRepContract, htmlREPcontracts = checkForRepCalcsSuccess()
    html = html + htmlBAI + htmlEDF + htmlREPcontracts

    html += """
    
        </table>
      </body>
    </html>
    """
    sendEmail(status,emailBodyReportEDF, emailBodyReportRepContract, html)

main()

