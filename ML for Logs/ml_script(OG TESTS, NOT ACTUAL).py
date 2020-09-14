#data_path = "C:\Users\fahmed\Desktop\ML for Logs\sample dataset"

import os
import random
import numpy as np



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
    random.seed(seed)
    random.shuffle(train_texts)
    random.seed(seed)
    random.shuffle(train_labels)
    #print(train_texts[0])
    #print(get_num_words_per_sample(train_texts))
    return ((train_texts, np.array(train_labels)),
            (test_texts, np.array(test_labels)))


x = load_dataset(r"C:\Users\fahmed\Desktop\ML for Logs\sample dataset")
X_train = x[0][0]
y_train = x[0][1]
X_test = x[1][0]
y_test = x[1][1]

import numpy
from keras_preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers.embeddings import Embedding



# fix random seed for reproducibility
numpy.random.seed(7)
# load the dataset but only keep the top n words, zero the rest
top_words = 1

# truncate and pad input sequences
max_review_length = 1
#X_train = sequence.pad_sequences(X_train, maxlen=max_review_length)
#X_test = sequence.pad_sequences(X_test, maxlen=max_review_length)



# create the model
embedding_vecor_length = 32
model = Sequential()
model.add(Embedding(top_words, embedding_vecor_length, input_length=max_review_length))
model.add(LSTM(100))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
print(model.summary())
model.fit(np.array(X_train), np.array(y_train), epochs=3, batch_size=64)
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))

