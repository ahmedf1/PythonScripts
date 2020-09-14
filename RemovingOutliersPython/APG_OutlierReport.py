#!/usr/bin/env python
# coding: utf-8

# In[22]:

###############################################################################
##                                                                           ##
##                          APG BILLED FILE TEST                             ##
##                                                                           ##
##                                                                           ##
###############################################################################

import pandas as pd
import numpy as np
from scipy import stats
import glob
import os

def APG_outlierDetection():

        list_of_files = glob.glob(r'\\prd-app-a01\d$\CE\Repcalcs\FTPFiles\Receivables\APG_Billed*.csv') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)


        if os.path.exists(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\APG_Billed_Outliers.txt'):
                os.remove(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\APG_Billed_Outliers.txt') #this deletes the file

        # create the file
        with open(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\APG_Billed_Outliers.txt', 'a') as fileToWrite:

            names = ["CustomerNumber", "LastInvoiceDate", "Billed 0-30", "31-60",
                 "61-90", "91-120", "121+", "POR", "RepID", "ProcessThruDate"
            ]

            df = pd.read_csv(latest_file, header = 0, delimiter = "|", names = names, na_values = "?")
            df.head()

            Q1 = df['Billed 0-30'].quantile(0.05)
            Q3 = df['Billed 0-30'].quantile(0.95)
            IQR = Q3 - Q1
            fileToWrite.write("File: " + latest_file + '\n\n')
            fileToWrite.write("Client: APG Billed " + '\n\n')
            fileToWrite.write("Computed IQR: " + str(IQR) + '\n')

            df2 = (df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))
            df3 = df2.loc[df2['Billed 0-30'] == True]
            List = []

            for row in df3.index:
                List.append(row)


            for num in List:
                if df.loc[num,'Billed 0-30'] > 20000 or df.loc[num,'Billed 0-30'] < -5000:
                    fileToWrite.write(str(df.loc[num]))
                    fileToWrite.write('\n\n')

            return latest_file

###############################################################################
##                                                                           ##
##                          APG UNBILLED FILE TEST                           ##
##                                                                           ##
##                                                                           ##
###############################################################################

def APG_UnbilledOutlierDetection():

        list_of_files = glob.glob(r'\\prd-app-a01\d$\CE\Repcalcs\FTPFiles\Receivables\APG_UnBilled*.csv') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)


        if os.path.exists(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\APG_UnBilled_Outliers.txt'):
                os.remove(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\APG_UnBilled_Outliers.txt') #this deletes the file

        # create the file
        with open(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\APG_UnBilled_Outliers.txt', 'a') as fileToWrite:

            names = ["Customer Number", "Unbilled Amount", "POR","RepID", "ProcessThruDate"]

            df = pd.read_csv(latest_file, header = 0, delimiter = "|", names = names, na_values = "?")
            df.head()

            Q1 = df["Unbilled Amount"].quantile(0.05)
            Q3 = df["Unbilled Amount"].quantile(0.95)
            IQR = Q3 - Q1
            fileToWrite.write("File: " + latest_file + '\n\n')
            fileToWrite.write("Client: APG Unbilled File" + '\n\n')
            fileToWrite.write("Computed IQR: " + str(IQR) + '\n')

            df2 = (df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))
            df3 = df2.loc[df2["Unbilled Amount"] == True]
            List = []

            for row in df3.index:
                List.append(row)


            for num in List:
                if df.loc[num,"Unbilled Amount"] > 10000 or df.loc[num,"Unbilled Amount"] < -1000:
                    fileToWrite.write(str(df.loc[num]))
                    fileToWrite.write('\n\n')

            return latest_file



