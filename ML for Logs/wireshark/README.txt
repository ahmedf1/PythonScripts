This project is using Machine Learning algorithms to analyze log report files and determine 
whether the process was a total success or had even a minor failure.

The idea is having the algorithm be able to identify what went wrong in the process without ever
having to open a log file.

And having a dashboard that displays the results of each log file
PRD
QA
BTB (this one will be hardest to process since the daily report is 
	added to the end of each file instead of just creating a new file)

First scope is just to distinguish between 0 errors and any errors at all.

Next step will be to classify the errors, so having outputs be 0 errors, connection errors, 
file missing errors, etc.