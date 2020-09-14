
import sys

sys.path.extend(('C:\\Users\\fahmed\\AppData\\Local\\Programs\\Python\\Python35\\Lib\\site-packages\\win32', 'C:\\Users\\fahmed\\AppData\\Local\\Programs\\Python\\Python35\\Lib\\site-packages\\win32\\lib', 'C:\\Users\\fahmed\\AppData\\Local\\Programs\\Python\\Python35\\Lib\\site-packages\\Pythonwin'))

import win32com.client

TASK_ENUM_HIDDEN = 1
TASK_STATE = {0: 'Unknown',
              1: 'Disabled',
              2: 'Queued',
              3: 'Ready',
              4: 'Running'}

scheduler = win32com.client.Dispatch('Schedule.Service')
scheduler.Connect()

n = 0
folders = [scheduler.GetFolder('\\')]
while folders:
    folder = folders.pop(0)
    folders += list(folder.GetFolders(0))
    tasks = list(folder.GetTasks(TASK_ENUM_HIDDEN))
    n += len(tasks)
    for task in tasks:
        if task.Path == r'\repSxdLoad':
            settings = task.Definition.Settings
            print('Path       : %s' % task.Path)
            print('Hidden     : %s' % settings.Hidden)
            print('State      : %s' % TASK_STATE[task.State])
            print('Last Run   : %s' % task.LastRunTime)
            print('Last Result: %s\n' % task.LastTaskResult)
            while TASK_STATE[task.State] == 'Running':
                print("Running")
            print("ran")
print('Listed %d tasks.' % n)
