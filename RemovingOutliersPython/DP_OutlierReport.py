#!/usr/bin/env python
# coding: utf-8

# In[22]:

###############################################################################
##                                                                           ##
##                          Discount BILLED FILE TEST                             ##
##                                                                           ##
##                                                                           ##
###############################################################################

import pandas as pd
import numpy as np
from scipy import stats
import glob
import os

def DP_outlierDetection():

        list_of_files = glob.glob(r'\\prd-app-a01\d$\CE\Repcalcs\FTPFiles\Receivables\AR_Detail_As_Of_Date_*.csv') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)


        if os.path.exists(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\DP_Billed_Outliers.txt'):
                os.remove(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\DP_Billed_Outliers.txt') #this deletes the file

        # create the file
        with open(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\DP_Billed_Outliers.txt', 'a') as fileToWrite:

            names = ["CLIENT_NAME", "CUSTOMER_NAME", "STATUS_DESC", "TERRITORY_CODE",
                 "LDC_ACCOUNT_NUM", "ACCOUNT", "UNSTATEMENTED", "DAYS_UNDER_30", "DAYS_30", "DAYS_60", "DAYS_90",
                 "DAYS_OVER_120", "BILLED_GE30", "BILLED_AR", "BILLED_BUDGET", "DEFERRED_AR", "ACTUAL_AR",
                 "RepID", "ProcessThruDate"
            ]

            df = pd.read_csv(latest_file, header = 0, delimiter = "|", names = names, na_values = "?")
            df.head()

            Q1 = df['BILLED_AR'].quantile(0.05)
            Q3 = df['BILLED_AR'].quantile(0.95)
            IQR = Q3 - Q1
            fileToWrite.write("File: " + latest_file + '\n\n')
            fileToWrite.write("Client: Discount Power Billed " + '\n\n')
            fileToWrite.write("Computed IQR: " + str(IQR) + '\n')

            df2 = (df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))
            df3 = df2.loc[df2['BILLED_AR'] == True]
            List = []

            for row in df3.index:
                List.append(row)


            for num in List:
                if df.loc[num,'BILLED_AR'] > 10000 or df.loc[num,'BILLED_AR'] < -1000:
                    fileToWrite.write(str(df.loc[num]))
                    fileToWrite.write('\n\n')
        return latest_file


###############################################################################
##                                                                           ##
##                          Discount UNBILLED FILE TEST                      ##
##                                                                           ##
##                                                                           ##
###############################################################################

def DP_UnbilledOutlierDetection():

        list_of_files = glob.glob(r'\\prd-app-a01\d$\CE\Repcalcs\FTPFiles\Receivables\UBL_DP_*.csv') # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)


        if os.path.exists(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\DP_UnBilled_Outliers.txt'):
                os.remove(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\DP_UnBilled_Outliers.txt') #this deletes the file

        # create the file
        with open(r'C:\Users\fahmed\Desktop\RemovingOutliersPython\DP_UnBilled_Outliers.txt', 'a') as fileToWrite:

            names = [
                "Zone", "Utility", "Date","WTD AVG", "Forecasted Revenue", "Revenue Correction", "Total"
                 , "Retail Load", "RepID", "ProcessThruDate"
            ]

            df = pd.read_csv(latest_file, header = 0, delimiter = "|", names = names, na_values = "?")
            df.head()

            #df = df[df.Total != '-'] #removing unwanted rows
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', -1)
            print(df)      
            print(df.dtypes)
            df.Total = df.Total.astype(float)
            print(df.dtypes)
            print(df)
            Q1 = df["Total"].quantile(0.05)
            
            Q3 = df["Total"].quantile(0.95)
            IQR = Q3 - Q1
            fileToWrite.write("File: " + latest_file + '\n\n')
            fileToWrite.write("Client: DP Unbilled File" + '\n\n')
            fileToWrite.write("Computed IQR: " + str(IQR) + '\n')

            df2 = (df < (Q1 - 1.5 * IQR)) |(df > (Q3 + 1.5 * IQR))
            df3 = df2.loc[df2["Total"] == True]
            List = []

            for row in df3.index:
                List.append(row)


            for num in List:
                if df.loc[num,"Total"] > 70000 or df.loc[num,"Total"] < -100:
                    fileToWrite.write(str(df.loc[num]))
                    fileToWrite.write('\n\n')
        return latest_file


