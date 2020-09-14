#!/usr/bin/env python
# coding: utf-8

# In[22]:

###############################################################################
##                                                                           ##
##                          VOLT BILLED FILE TEST                             ##
##                                                                           ##
##                                                                           ##
###############################################################################

import pandas as pd
import numpy as np
from scipy import stats
import glob
import os

def VOLT_outlierDetection():

        list_of_files = glob.glob(r'\\prd-app-a01\d$\CE\Repcalcs\FTPFiles\Receivables\* Billed.csv') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)


        if os.path.exists(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\Volt_Billed_Outliers.txt'):
                os.remove(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\Volt_Billed_Outliers.txt') #this deletes the file

        # create the file
        with open(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\Volt_Billed_Outliers.txt', 'a') as fileToWrite:

            names = ["Account ID", "Plan Group", "Customer Status", "Pay Term",
                 "Total Due Amount", "Current Due Amount", "0-10days", "11-30days", "31-60days", "61-90days", "91-120days",
                 "121-150days", "151-180days", "MoreThan180days", "Days Past Due", "Create Date", "RepID", "ProcessThruDate"
            ]

            df = pd.read_csv(latest_file, header = 0, delimiter = "|", names = names, na_values = "?")
            df.head()
            
            
            df2 = df[["Total Due Amount", "31-60days", "61-90days", "91-120days", "121-150days", "151-180days", "MoreThan180days"]]

            df2["Billed 0-30"] = df2["Total Due Amount"].astype(float) - (df2["31-60days"].astype(float) + df2["61-90days"].astype(float) + df2["91-120days"].astype(float) + df2["121-150days"].astype(float) + df2["151-180days"].astype(float) + df2["MoreThan180days"].astype(float))

            

            Q1 = df2['Billed 0-30'].quantile(0.05)
            Q3 = df2['Billed 0-30'].quantile(0.95)
            IQR = Q3 - Q1
            fileToWrite.write("File: " + latest_file + '\n\n')
            fileToWrite.write("Client: VOLT Billed" + '\n\n')
            fileToWrite.write("Computed IQR: " + str(IQR) + '\n')

            df3 = (df2 < (Q1 - 1.5 * IQR)) |(df2 > (Q3 + 1.5 * IQR))
            df4 = df3.loc[df3['Billed 0-30'] == True]
            List = []

            for row in df4.index:
                List.append(row)


            for num in List:
                if df2.loc[num,'Billed 0-30'] > 2000 or df2.loc[num,'Billed 0-30'] < -1000:
                    fileToWrite.write(str(df2.loc[num]))
                    fileToWrite.write('\n\n')

        return latest_file
###############################################################################
##                                                                           ##
##                          VOLT UNBILLED FILE TEST                           ##
##                                                                           ##
##                                                                           ##
###############################################################################

def Volt_UnbilledOutlierDetection():

        list_of_files = glob.glob(r'\\prd-app-a01\d$\CE\Repcalcs\FTPFiles\Receivables\* UnBilled.csv') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        print(latest_file)

        if os.path.exists(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\Volt_UnBilled_Outliers.txt'):
                os.remove(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\Volt_UnBilled_Outliers.txt') #this deletes the file

        # create the file
        with open(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\Volt_UnBilled_Outliers.txt', 'a') as fileToWrite:

            names = ["Account Number", "Total Consumption KWH","Account Class", "Account Type", "Account Status", "Unbilled"]

            df = pd.read_csv(latest_file, header = 0, delimiter = ",", names = names, na_values = "?")
            df.head()

            Q1 = df["Unbilled"].quantile(0.05)
            Q3 = df["Unbilled"].quantile(0.95)
            IQR = Q3 - Q1
            fileToWrite.write("File: " + latest_file + '\n\n')
            fileToWrite.write("Client: Volt Unbilled File" + '\n\n')
            fileToWrite.write("Computed IQR: " + str(IQR) + '\n')

            df2 = (df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))
            df3 = df2.loc[df2["Unbilled"] == True]
            List = []

            for row in df3.index:
                List.append(row)


            for num in List:
                if df.loc[num,"Unbilled"] > 1000 or df.loc[num,"Unbilled"] < -100:
                    fileToWrite.write(str(df.loc[num]))
                    fileToWrite.write('\n\n')

        return latest_file



print(Volt_UnbilledOutlierDetection())

