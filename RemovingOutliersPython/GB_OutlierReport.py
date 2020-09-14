#!/usr/bin/env python
# coding: utf-8

# In[22]:

###############################################################################
##                                                                           ##
##                          GB BILLED FILE TEST                             ##
##                                                                           ##
##                                                                           ##
###############################################################################

import pandas as pd
import numpy as np
import seaborn as sns
from scipy import stats
import glob
import os

def GBP_outlierDetection():

        list_of_files = glob.glob(r'\\prd-app-a01\d$\CE\Repcalcs\FTPFiles\Receivables\*_VantageBilled.csv') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)

        print(latest_file)

        if os.path.exists(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\GB_Power_Billed_Outliers.txt'):
                os.remove(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\GB_Power_Billed_Outliers.txt') #this deletes the file

        # create the file
        with open(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\GB_Power_Billed_Outliers.txt', 'a') as fileToWrite:

            names = ["MARKETER ACCOUNT NUMBER", "DISPLAY NAME", "UTILITY NAME",
                 "TOTAL DUE AMOUNT", "0_10 DAYS", "11_30 DAYS", "31_60 DAYS", "61_90 DAYS", "91_120 DAYS",
                 "121_150 DAYS", "151_180 DAYS", "MORE THAN 180 DAYS", "LAST PAYMENT DATE",
                 "LAST PAY AMOUNT", "Contact Name", "PHONE 1", "Sales Person 1", "Sales Person 2",
                    "Customer Status", "Account Type", "Account Class", "BILL PRESENTMENT", "CUSTOMERSTART DATE",
                     "CusInfo1", "CusInfo2", "CusInfo3", "CusInfo4", "CusInfo5", "POR Account", "Last Bill Date",
                     "Last Bill Amount", "Billing Name", "EMAIL ID", "ADDRESS", "Credit Score", "CITY", "STATE",
                     "ZIP", "CREDIT RATING", "CREDIT RATING2", "CREDIT RATING3", "CREDIT RATING4", "CUSTOMEREND DATE",
                     "NO. OF DAYS INACTIVE", "LOCKBOX", "BILL TYPE", "GROUP NAME", "LAST STATEMENT DATE",
                     "Distribution Group", "PREMISE ID", "PHONE 2", "TOTAL INV AMOUNT", "DEBIT ADJ", "CREDIT ADJ",
                     "PAY TERM", "CURRENT DUE AMOUNT", "DAYS PAST DUE", "CREDIT ID", "RepID", "ProcessThruDate"
,            ]

            df = pd.read_csv(latest_file, header = 0, delimiter = "|")#, names = names, na_values = "?")
            df.head()
            
            
            df2 = df[["TOTAL DUE AMOUNT", "0_10 DAYS", "11_30 DAYS", "31_60 DAYS", "61_90 DAYS", "91_120 DAYS", "121_150 DAYS", "151_180 DAYS", "MORE THAN 180 DAYS",]]

            df2["Billed 0-30"] = df2["TOTAL DUE AMOUNT"].astype(float) - (df2["31_60 DAYS"].astype(float) + df2["61_90 DAYS"].astype(float) + df2["91_120 DAYS"].astype(float) + df2["121_150 DAYS"].astype(float) + df2["151_180 DAYS"].astype(float) + df2["MORE THAN 180 DAYS"].astype(float))

            

            Q1 = df2['Billed 0-30'].quantile(0.05)
            Q3 = df2['Billed 0-30'].quantile(0.95)
            IQR = Q3 - Q1
            fileToWrite.write("File: " + latest_file + '\n\n')
            fileToWrite.write("Client: GB Power Billed" + '\n\n')
            fileToWrite.write("Computed IQR: " + str(IQR) + '\n')

            df3 = (df2 < (Q1 - 1.5 * IQR)) |(df2 > (Q3 + 1.5 * IQR))
            df4 = df3.loc[df3['Billed 0-30'] == True]
            List = []

            for row in df4.index:
                List.append(row)


            for num in List:
                if df2.loc[num,'Billed 0-30'] > 7000 or df2.loc[num,'Billed 0-30'] < -1000:
                    fileToWrite.write(str(df2.loc[num]))
                    fileToWrite.write('\n\n')
        return latest_file
  

###############################################################################
##                                                                           ##
##                          GB UNBILLED FILE TEST                           ##
##                                                                           ##
##                                                                           ##
###############################################################################

def GBP_UnbilledOutlierDetection():

        list_of_files = glob.glob(r'\\prd-app-a01\d$\CE\Repcalcs\FTPFiles\Receivables\*_VantageUnBilled.csv') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)


        if os.path.exists(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\GB_Power_UnBilled_Outliers.txt'):
                os.remove(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\GB_Power_UnBilled_Outliers.txt') #this deletes the file

        # create the file
        with open(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\GB_Power_UnBilled_Outliers.txt', 'a') as fileToWrite:

            names = ["Customer Name", "Marketer Account Number","Utility Account Number", "Meter Number", "Reading Start Date",
                     "Reading End Date", "Unbilled Days", "Unit Status", "Customer Status", "Utility", "Sales Person",
                     "Customer Start Date", "Usage Amount", "Usage Start Date", "Usage End Date", "Energy Rate", "Avg Daily Usage",
                     "Unbilled Amount", "Commodity", "POR", "Last Invoice Date", "Last Invoice Number", "Last Invoice charge amount",
                     "Credit Score", "RepID", "ProcessThruDate"
                     ]

            df = pd.read_csv(latest_file, header = 0, delimiter = "|")#, names = names, na_values = "?")
            df.head()

            df2 = df[["Marketer Account Number", "Usage Amount", "Unbilled Amount", "Last Invoice Date", "RepID", "ProcessThruDate"]]

            Q1 = df2["Unbilled Amount"].quantile(0.05)
            Q3 = df2["Unbilled Amount"].quantile(0.95)
            IQR = Q3 - Q1
            fileToWrite.write("File: " + latest_file + '\n\n')
            fileToWrite.write("Client: GB POWER Unbilled File" + '\n\n')
            fileToWrite.write("Computed IQR: " + str(IQR) + '\n')

            df3 = (df2 < (Q1 - 1.5 * IQR)) |(df2 > (Q3 + 1.5 * IQR))
            df4 = df3.loc[df2["Unbilled Amount"] == True]
            List = []

            for row in df3.index:
                List.append(row)


            for num in List:
                if df2.loc[num,"Unbilled Amount"] > 10000 or df2.loc[num,"Unbilled Amount"] < -100:
                    fileToWrite.write(str(df2.loc[num]))
                    fileToWrite.write('\n\n')
        return latest_file






