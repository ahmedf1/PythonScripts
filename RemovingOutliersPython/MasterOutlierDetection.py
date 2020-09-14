import APG_OutlierReport
import VOLT_OutlierReport
import DP_OutlierReport
import GB_OutlierReport
import os
import datetime
# libraries to be imported 
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import datetime
import pyodbc

def getActiveClientsFromDB():
    text = ''
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
            text = text + "Successful Billed insert for repID " + str(repID) + "\n"
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
            text = text + "Successful UnBilled insert for repID " + str(repID) + "\n"
        activeClients = []
    cnxn.close()
    return text

def main():
    # get date for file name matching
    today = datetime.date.today()
    month = today.strftime("%m")
    year = today.strftime("%Y")
    day = today.strftime("%d")
    
    
    # commented out so that the master outlier log will compile the list of all insert results
    # will help troubleshoot and figure out why it runs some days and not others
    #if os.path.exists(r'C:\Users\fahmed\Desktop\Removing Outliers Python\MasterOutlierLog.txt'):
     #   os.remove(r'C:\Users\fahmed\Desktop\Removing Outliers Python\MasterOutlierLog.txt') #this deletes the file

    with open(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\MasterOutlierLog.txt', 'w') as fileToWrite:
        dateTimeNow = str(datetime.datetime.today().date()) + " 03:59:59"
        fileToWrite.write("ProcessThruDate: " + dateTimeNow)


        try:
            fileToWrite.write("\n\nRunning for APG Billed\n")
            latestFileAPG_Billed = APG_OutlierReport.APG_outlierDetection()
            fileToWrite.write("Success!\n\n")
        except Exception as e:
            fileToWrite.write("Failure! The following error occured:\n" + str(e))
            
        try:    
            fileToWrite.write("\n\nRunning for APG UnBilled\n")
            latestFileAPG_Unbilled = APG_OutlierReport.APG_UnbilledOutlierDetection()
            fileToWrite.write("Success!\n\n")
        except Exception as e:
            fileToWrite.write("Failure! The following error occured:\n" + str(e))
        
        ## APG File Format = APG_Billed_06-17-2019.csv
        APG_billedPTD_fileName = "APG_Billed_" + month + "-" + day + "-" + year + ".csv"
        APG_unbilledPTD_fileName = "APG_Unbilled_" + month + "-" + day + "-" + year + ".csv"
        print(APG_unbilledPTD_fileName)
        print(latestFileAPG_Unbilled)
        
        ## insert and match the file to the date
        isAPGBilled = True if APG_billedPTD_fileName in latestFileAPG_Billed else False
        isAPGUnbilled = True if APG_unbilledPTD_fileName in latestFileAPG_Unbilled else False
        
        
        try:
            fileToWrite.write("\n\nRunning for Volt Billed\n")
            latestFileVolt_Billed = VOLT_OutlierReport.VOLT_outlierDetection()
            fileToWrite.write("Success!\n\n")
        except Exception as e:
            fileToWrite.write("Failure! The following error occured:\n" + str(e))

        try:
            fileToWrite.write("\n\nRunning for Volt UnBilled\n")
            latestFileVolt_Unbilled = VOLT_OutlierReport.Volt_UnbilledOutlierDetection()
            fileToWrite.write("Success!\n\n")
        except Exception as e:
            fileToWrite.write("Failure! The following error occured:\n" + str(e))
            
        Volt_billedPTD_fileName = "" + month + day + year + " Billed.csv"
        Volt_unbilledPTD_fileName = "" + month + day + year + " UnBilled.csv"

        ## insert and match the file to the date
        isVoltBilled = True if Volt_billedPTD_fileName in latestFileVolt_Billed else False
        isVoltUnbilled = True if Volt_unbilledPTD_fileName in latestFileVolt_Unbilled else False

        try:
            fileToWrite.write("\n\nRunning for Discount Power Billed\n")
            latestFileDP_Billed = DP_OutlierReport.DP_outlierDetection()
            fileToWrite.write("Success!\n\n")
        except Exception as e:
            fileToWrite.write("Failure! The following error occured:\n" + str(e))

        try:
            fileToWrite.write("\n\nRunning for Discount Power UnBilled\n")
            latestFileDP_Unbilled = DP_OutlierReport.DP_UnbilledOutlierDetection()
            fileToWrite.write("Success!\n\n")
        except Exception as e:
            fileToWrite.write("Failure! The following error occured:\n" + str(e))
        
        dayMinus1 = int(day)-1
        if dayMinus1 < 10:
            dayMinus1 = "0" + str(dayMinus1)
        
        DP_billedPTD_fileName = "AR_Detail_As_Of_Date_" + year + "-" + month + "-" + str(dayMinus1)
        DP_unbilledPTD_fileName = "UBL_DP_" + year + month +  str(dayMinus1) + ".csv"
        
        ## insert and match the file to the date
        isDPBilled = True if DP_billedPTD_fileName in latestFileDP_Billed else False
        isDPUnbilled = True if DP_unbilledPTD_fileName in latestFileDP_Unbilled else False
        print(isDPBilled)
        print(DP_billedPTD_fileName)
        print(latestFileDP_Billed)

        print('\n\n')
        print(isDPUnbilled)
        print(DP_unbilledPTD_fileName)
        print(latestFileDP_Unbilled)
        
        try:
            fileToWrite.write("\n\nRunning for GB Power Billed\n")
            latestFileGBP_Billed = GB_OutlierReport.GBP_outlierDetection()
            fileToWrite.write("Success!\n\n")
        except Exception as e:
            fileToWrite.write("Failure! The following error occured:\n" + str(e))

        try:
            fileToWrite.write("\n\nRunning for GB Power UnBilled\n")
            latestFileGBP_Unbilled = GB_OutlierReport.GBP_UnbilledOutlierDetection()
            fileToWrite.write("Success!\n\n")
        except Exception as e:
            fileToWrite.write("Failure! The following error occured:\n" + str(e))
        
        GBP_billedPTD_fileName = "" + year[2] + year[3]  + month + day #+ "0001_VantageBilled.csv"          can take out these since GB Power tends to change
        GBP_unbilledPTD_fileName = "" + year[2] + year[3] + month + day #+ "0002_VantageUnbilled.csv"       the numbers randomly, mainly the '1' or '2'

        ## insert and match the file to the date
        isGBPBilled = True if GBP_billedPTD_fileName in latestFileGBP_Billed else False
        isGBPUnbilled = True if GBP_unbilledPTD_fileName in latestFileGBP_Unbilled else False

        emailBodyReport = ""
        if not isAPGBilled: emailBodyReport += "Missing APG BILLED FILE\n"
        if not isAPGUnbilled: emailBodyReport += "Missing APG UNBILLED FILE\n"
        if not isVoltBilled: emailBodyReport += "Missing VOLT BILLED FILE\n"
        if not isVoltUnbilled: emailBodyReport += "Missing VOLT UNBILLED FILE\n"
        if not isDPBilled: emailBodyReport += "Missing DISCOUNT POWER BILLED FILE\n"
        if not isDPUnbilled: emailBodyReport += "Missing DISCOUNT POWER UNBILLED FILE\n"
        if not isGBPBilled: emailBodyReport += "Missing GB POWER BILLED FILE\n"
        if not isGBPUnbilled: emailBodyReport += "Missing GB POWER UNBILLED FILE\n"

        emailBodyReport += "\n\n" + getActiveClientsFromDB()
        
        sendEmail_V1(emailBodyReport)       # Email to Jasdev
        sendEmail_V2(emailBodyReport)       # Email to self

#Python code to illustrate Sending mail with attachments 
# from your Gmail account  

def sendEmail_V1(emailBodyReport):
   
    fromaddr = "fahmed@vantagecommodities.com"
    toaddr = "jsingh@vantagecommodities.com"
    
   
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 
  
    # storing the senders email address   
    msg['From'] = fromaddr 
  
    # storing the receivers email address  
    msg['To'] = toaddr 
  
    # storing the subject  
    msg['Subject'] = "Reporting Outliers From AR Files" 
      
    # string to store the body of the mail 
    # string to store the body of the mail
    body = "Outlier Reporting for "+ str(datetime.datetime.today().date()) + '\n\n'
    if emailBodyReport != "":
         body += emailBodyReport
    else:
        body += "No missing files to report!"
  
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
  
    # open the file to be sent
    filenames = [
        r"C:\Users\fahmed\Desktop\RemovingOutliersPython\APG_Billed_Outliers.txt"
        , r"C:\Users\fahmed\Desktop\RemovingOutliersPython\APG_UnBilled_Outliers.txt"
        , r"C:\Users\fahmed\Desktop\RemovingOutliersPython\Volt_Billed_Outliers.txt"
        , r"C:\Users\fahmed\Desktop\RemovingOutliersPython\Volt_UnBilled_Outliers.txt"
        , r"C:\Users\fahmed\Desktop\RemovingOutliersPython\DP_Billed_Outliers.txt"
        , r"C:\Users\fahmed\Desktop\RemovingOutliersPython\DP_UnBilled_Outliers.txt"
        , r"C:\Users\fahmed\Desktop\RemovingOutliersPython\GB_Power_Billed_Outliers.txt"
        , r"C:\Users\fahmed\Desktop\RemovingOutliersPython\GB_Power_UnBilled_Outliers.txt"

    ]

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
        
def sendEmail_V2(emailBodyReport):
   
    fromaddr = "fahmed@vantagecommodities.com"
    toaddr = "fahmed@vantagecommodities.com"
    
   
    # instance of MIMEMultipart 
    msg = MIMEMultipart() 
  
    # storing the senders email address   
    msg['From'] = fromaddr 
  
    # storing the receivers email address  
    msg['To'] = toaddr 
  
    # storing the subject  
    msg['Subject'] = "Reporting Outliers From AR Files" 
      
    # string to store the body of the mail
    body = "Outlier Reporting for "+ str(datetime.datetime.today().date()) + '\n\n'
    if emailBodyReport != "":
         body += emailBodyReport
    else:
        body += "No missing files to report!"
  
    # attach the body with the msg instance 
    msg.attach(MIMEText(body, 'plain')) 
  
    # open the file to be sent
    filenames = [
        r"C:\Users\fahmed\Desktop\RemovingOutliersPython\APG_Billed_Outliers.txt"
        , r"C:\Users\fahmed\Desktop\RemovingOutliersPython\APG_UnBilled_Outliers.txt"
        , r"C:\Users\fahmed\Desktop\RemovingOutliersPython\Volt_Billed_Outliers.txt"
        , r"C:\Users\fahmed\Desktop\RemovingOutliersPython\Volt_UnBilled_Outliers.txt"
        , r"C:\Users\fahmed\Desktop\RemovingOutliersPython\DP_Billed_Outliers.txt"
        , r"C:\Users\fahmed\Desktop\RemovingOutliersPython\DP_UnBilled_Outliers.txt"
        , r"C:\Users\fahmed\Desktop\RemovingOutliersPython\GB_Power_Billed_Outliers.txt"
        , r"C:\Users\fahmed\Desktop\RemovingOutliersPython\GB_Power_UnBilled_Outliers.txt"
    ]

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


main()
