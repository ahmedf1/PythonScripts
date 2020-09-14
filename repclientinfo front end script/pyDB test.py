server_name = "qa-sqlp-a01";
User = "repcalcs";
password = "filt123";
db_name = "Rules";

import os
import webbrowser


import pyodbc
import pandas as pd
pd.set_option('colheader_justify', 'center')   # FOR TABLE <th>

cnxn = pyodbc.connect("Driver={SQL Server};"
                      "Server=qa-sqlp-a01;"
                      "Database=Rules;"
                      "Trusted_Connection=yes;"
					  "uid=repcalcs;pwd=filt123")

df = pd.read_sql_query(""" SELECT c.ParticipantId, s.shortClientName, c.Active, c.ActiveCerts, c.POR, username=s.UserName, password=s.SFTP_Password, EmailAddress=ISNULL(s.EmailAddress,''), 
        ActiveContact=ISNULL(c.Active,0), c.sftp ,c.reports
        FROM APX2000.dbo.cfg_RepClients c
		JOIN Rules.dbo.cfg_RepClient_InfoandSFTP s ON c.ParticipantId = s.RepId
        ORDER BY c.ParticipantId ASC""", cnxn)


html_string = '''
<html>
<style>
.mystyle {
    font-size: 11pt; 
    font-family: Arial;
    border-collapse: collapse; 
    border: 1px solid silver;

}

.mystyle td, th {
    padding: 5px;
}

.mystyle tr:nth-child(even) {
    background: #E0E0E0;
}

.mystyle tr:hover {
    background: silver;
    cursor: pointer;
}

.green{
	background-color:green;
}
</style>
  <head><title>Client SFTP Mailbox Credentials</title></head>
  <link rel="stylesheet" type="text/css" href="df_style.css"/>
  <script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>
  <script src="myscripts.js"></script>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
  <body>
  <div class="jumbotron">Here you can find each client's mailbox credentials as well as</div>

    <div class="d-flex justify-content-center">
    <div class = "form-check">
    <input type="checkbox" class="form-check-input" id="exampleCheck1" onclick="filtertoActiveClients()">
    <label class="form-check-label" for="exampleCheck1">Filter to Active Clients Only</label>
    </div>
    </div>
    <div class="d-flex justify-content-center">
    <div class = "form-check">
    <input type="checkbox" class="form-check-input" id="exampleCheck2" onclick="filtertoUnassignedMailboxes()">
    <label class="form-check-label" for="exampleCheck2">Show Unassigned Mailboxes</label>
    </div>
    </div>


    <div class ="d-flex justify-content-center">
    {table}
    </div>
  </body>
</html>
'''

path = os.path.abspath('temp.html')
url = 'file://' + path

with open(path, 'w') as f:
    f.write(html_string.format(table=df.to_html(table_id="clientTable")))
webbrowser.open(url)


