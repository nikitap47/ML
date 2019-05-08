# -*- coding: utf-8 -*-
from sklearn import metrics
import keras
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf
from keras import layers
import sklearn
from sklearn.preprocessing import LabelBinarizer
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
import keras.layers as km
 
data = pd.read_csv('new_dataset.csv')

X = data.iloc[:,:-1].values
y = data.iloc[:,-1].values

X_new = np.empty((5200,35))
Y = np.chararray((5200,1))
m = np.chararray((5200,26))
j = 0
for i in range(0,5199):
    x = np.matrix(X[j:j+5,:])
    X_new[i,:] = np.reshape(x.T,-1,35)
    Y[i] = y[j]
    j= j + 5

lb = sklearn.preprocessing.LabelBinarizer()    
encoder = LabelBinarizer()
decoder = LabelBinarizer()
transformed_label = encoder.fit_transform(Y)

X_train, X_test, y_train, y_test = train_test_split(X_new, transformed_label, test_size=0.2)
X_train = tf.keras.utils.normalize(X_train, axis=1)  # scales data between 0 and 1
X_test = tf.keras.utils.normalize(X_test, axis=1) 
model = Sequential()

model.add(Dense(35, activation='relu',input_dim = 35))
model.add(Dense(124, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(27, activation='softmax'))
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
results = model.fit(X_train, y_train, epochs=60,validation_data=(X_test,y_test))

loss_and_metrics = model.evaluate(X_test, y_test, batch_size=128)
model.save('sign_detector.model')
new_model = tf.keras.models.load_model('sign_detector.model')
predictions = new_model.predict(X_train)

l = ['0','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
#L = (np.argmax(predictions[0]))
for i in range(0,448):
    v = np.argmax(predictions[i])
    print(l[int(v)])






