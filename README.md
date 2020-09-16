# Vantage Python Scripts #

This repository contains all scripts that were written to assist in Vantage operations.

### Daily Log Reporting ###
This collection of python scripts retrieves Active Clients via a database connection, and then uses their repID values to retrieve the individual log sections from both RepCalcs and EdfDump and writes the sections to their own txt files. These files are then attached to an email message and sent out using SMTP every morning at 8AM.

### ML for Logs ###
These scripts use machine learning libraries to parse log files produced daily by EDFDump and RepCalcs to determine whether there were any errors in the automated execution of the aforementioned C# programs.

### Removing Outliers Python ###
This script queries active clients from the database and runs outlier detection on the data contained in their respective Billed and Unbilled Receivables files. This script writes the outliers and their corresponding row of data to a text file and attaches them to an email message which is then fired off using SMTP to email the outliers and report which clients are missing/ have not uploaded their daily receivables files.

### WebScraping ###
This script was never launched into production but was designed to use the selenium library to do gather profile data from LinkedIn, given certain specified search parameters.

### Rep Client Info Front End Script ###
This script uses Jupyter notebook to query the database and retrieve all SFTP data, including all mailboxes as well as login and password information. This script is currently active and running on a Confluence page, which acts as a shortcut for retrieving SFTP data.

### Vantage Process GUI ###
This script creates a GUI for all processes, which may be viewed depending on the option that is selected. Functionality is in place for EDFDump, RepCalcs, and BuildTheBank processes.

### Task Scheduler APIs ###
There are two scripts that are both APIs for the Windows Task Scheduler. A third script RecvRetry.py utilizes these two APIs to gather tasks that have their state as “Runnning” while the python script is executing.


