from sklearn import model_selection, preprocessing, linear_model, naive_bayes, metrics, svm
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn import decomposition, ensemble

import os, random
import pandas, string
import xgboost
import numpy as np
from keras.preprocessing import text, sequence
from keras import layers, models, optimizers
import exportStatusToDashboard
import statistics
from joblib import *
import datetime

# load the PRD EDFDump file and turn it into a dataframe using numpy library

def load_PRDfile_toPredict():
    file_toPredict=[]
    with open(r'\\prd-app-a01\d$\CE\EDFDump\EDFDump.log') as f:
        file_toPredict.append(f.read())
        df2 = np.array(file_toPredict)
        df2.reshape(1, -1)
    return df2

def load_QAfile_toPredict():
    file_toPredict=[]
    with open(r'\\qa-app-a01\d$\CE\EDFDump\EDFDump.log') as f:
        file_toPredict.append(f.read())
        df2 = np.array(file_toPredict)
        df2.reshape(1, -1)
    return df2

classifier = load(r'C:\Users\fahmed\Desktop\ML for Logs\EDFDumpClassifier.joblib')
tfidf_vect = load(r'C:\Users\fahmed\Desktop\ML for Logs\EDFDumpVocabVectorizer.joblib')
acc = load(r'C:\Users\fahmed\Desktop\ML for Logs\EDFDumpModelAccuracy.joblib')



dfPRD = load_PRDfile_toPredict()
dfQA = load_QAfile_toPredict()


dfPRD = tfidf_vect.transform(dfPRD)
dfQA = tfidf_vect.transform(dfQA)

print("ACCURACY OF MODEL = " + str(acc))

edfDumpStatusPRD = []
for i in range(0,3):
    prediction = classifier.predict(dfPRD)
    edfDumpStatusPRD.append(int(prediction))
    
edfDumpStatusModePRD = max(set(edfDumpStatusPRD), key=edfDumpStatusPRD.count)
print(str(datetime.date.today()) + " PRD ")
print(edfDumpStatusPRD)
print(edfDumpStatusModePRD)
print('\n')

edfDumpStatusQA = []
for i in range(0,3):
    prediction = classifier.predict(dfQA)
    edfDumpStatusQA.append(int(prediction))

edfDumpStatusModeQA = max(set(edfDumpStatusQA), key=edfDumpStatusQA.count)
print(str(datetime.date.today()) + " QA ")
print(edfDumpStatusQA)
print(edfDumpStatusModeQA)


PTD = str(datetime.date.today())

prdStatus = "Success" if edfDumpStatusModePRD == 1 else "Small Issue"
qaStatus = "Success" if edfDumpStatusModeQA == 1 else "Small Issue"

f = open(r"C:\Users\fahmed\Desktop\output.txt","a+")
lineToWrite = PTD + '\t' + "EDFDump" + '\t' +'\t'+ "PRD" + '\t' +'\t'+ ("Success" if edfDumpStatusModePRD == 1 else "Failed/ERROR") + "\t ACCURACY: " + str(acc) + '\n'
f.write(lineToWrite)
lineToWrite = PTD + '\t' + "EDFDump" + '\t' +'\t'+ "QA" + '\t' +'\t'+ ("Success" if edfDumpStatusModeQA == 1 else "Failed/ERROR") + "\t ACCURACY: " + str(acc) + '\n'
f.write(lineToWrite)
f.close()
exportStatusToDashboard.main(prdStatus, qaStatus, PTD, 0)

