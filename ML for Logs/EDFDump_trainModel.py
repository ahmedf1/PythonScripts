'''
    Since it is desirable to maintain a model after training instead of always
    retraining, this script will serve to train the model and store it using
    pickle library.

    Pickle is used to store python objects into files for later use.

    The previous file, ml_try2.py (will be renamed eventually) will just serve
    to make the prediction. All training will go here so that the model is
    not trained everyday.
    
'''
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
import pickle
from joblib import *
import datetime

def load_dataset(data_path, seed=123):

    data = os.path.join(data_path, 'edf')

    # Load the training data
    train_texts = []
    train_labels = []
    for category in ['Failed', 'Success']:
        train_path = os.path.join(data, 'training set', category)
        for fname in sorted(os.listdir(train_path)):
            if fname.endswith('.log'):
                with open(os.path.join(train_path, fname)) as f:
                    train_texts.append(f.read().replace(",", " "))
                train_labels.append(0 if category == 'Failed' else 1)

    # Load the validation data.
    test_texts = []
    test_labels = []
    for category in ['Failed', 'Success']:
        test_path = os.path.join(data, 'test set', category)
        for fname in sorted(os.listdir(test_path)):
            if fname.endswith('.log'):
                with open(os.path.join(test_path, fname)) as f:
                    test_texts.append(f.read().replace(",", " "))
                test_labels.append(0 if category == 'Failed' else 1)

    # Shuffle the training data and labels.
    #random.seed(seed)
    #random.shuffle(train_texts)
    #random.seed(seed)
    #random.shuffle(train_labels)
    #print(train_texts[0])
    #print(get_num_words_per_sample(train_texts))
    return ((train_texts, np.array(train_labels)),
            (test_texts, np.array(test_labels)))

x = load_dataset(r"C:\Users\fahmed\Desktop\ML for Logs\sample dataset")

# create a dataframe using texts and lables
trainDF = pandas.DataFrame()
trainDF['text'] = x[0][0]
trainDF['label'] = x[0][1]

# split the dataset into training and validation datasets 
train_x, valid_x, train_y, valid_y = model_selection.train_test_split(trainDF['text'], trainDF['label'])

# label encode the target variable 
encoder = preprocessing.LabelEncoder()
train_y = encoder.fit_transform(train_y)

valid_y = encoder.fit_transform(valid_y)

# create a count vectorizer object 
count_vect = CountVectorizer(analyzer='word', token_pattern=r'\w{1,}')
count_vect.fit(trainDF['text'])

# transform the training and validation data using count vectorizer object
xtrain_count =  count_vect.transform(train_x)
xvalid_count =  count_vect.transform(valid_x)

def train_model(classifier, feature_vector_train, label, feature_vector_valid, is_neural_net=False):
    # fit the training dataset on the classifier
    classifier.fit(feature_vector_train, label)
    
    # predict the labels on validation dataset
    predictions = classifier.predict(feature_vector_valid)
    
    if is_neural_net:
        predictions = predictions.argmax(axis=-1)
    acc = metrics.accuracy_score(predictions, valid_y)
    #print ("LR, Count Vectors: ", metrics.accuracy_score(predictions, valid_y))
    return classifier, acc


# word level tf-idf
tfidf_vect = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', max_features=5000)
tfidf_vect.fit(trainDF['text'])
xtrain_tfidf =  tfidf_vect.transform(train_x)
xvalid_tfidf =  tfidf_vect.transform(valid_x)

# ngram level tf-idf 
tfidf_vect_ngram = TfidfVectorizer(analyzer='word', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=5000)
tfidf_vect_ngram.fit(trainDF['text'])
xtrain_tfidf_ngram =  tfidf_vect_ngram.transform(train_x)
xvalid_tfidf_ngram =  tfidf_vect_ngram.transform(valid_x)

# characters level tf-idf
tfidf_vect_ngram_chars = TfidfVectorizer(analyzer='char', token_pattern=r'\w{1,}', ngram_range=(2,3), max_features=5000)
tfidf_vect_ngram_chars.fit(trainDF['text'])
xtrain_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(train_x) 
xvalid_tfidf_ngram_chars =  tfidf_vect_ngram_chars.transform(valid_x) 


# Naive Bayes on Count Vectors
#classifier = train_model(linear_model.LogisticRegression(), xtrain_count, train_y, xvalid_count)
#print ("LR, Count Vectors: ", accuracy)


# Extereme Gradient Boosting on Word Level TF IDF Vectors
classifier, acc = train_model(xgboost.XGBClassifier(), xtrain_tfidf.tocsc(), train_y, xvalid_tfidf.tocsc())
#print ("Xgb, WordLevel TF-IDF: ", accuracy)

print("ACCURACY OF MODEL = " + str(acc))
dump(str(acc), 'EDFDumpModelAccuracy.joblib')
dump(classifier, 'EDFDumpClassifier.joblib')
dump(tfidf_vect, 'EDFDumpVocabVectorizer.joblib')


