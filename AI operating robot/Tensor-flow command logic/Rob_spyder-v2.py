# -*- coding: utf-8 -*-
#"""
#Created on Sun Jan 30 21:01:08 2022

#@author: Paulo Vicente Valente (paulo.valente@gmail.com)
#"""


import serial
import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from matplotlib import rcParams
from keras.models import Sequential, save_model, load_model
from keras.layers import Dense
import time


X_train = pd.read_csv('C:/Users/pvval/sensor.txt', header=None)
Y_train = pd.read_csv('C:/Users/pvval/commandfile.txt', header=None)

X_train_len_line=len(X_train)
#X_train_len_col=len(X_train.columns)
X_train_len_col=6
X_train_treated = np.zeros((X_train_len_line,6), dtype=float)
Y_train_treated = np.zeros((X_train_len_line,4), dtype=float)
X_train_treated_prize = np.zeros((X_train_len_line,1), dtype=float)

num = 0
while num < X_train_len_line:
  #print (num)

  if X_train.at[num,1]<=20:
    X_train_treated[num,0] = 0
  else: X_train_treated[num,0] = 1

  if X_train.at[num,2]<=10:
    X_train_treated[num,1] = 0
  else: X_train_treated[num,1] = 1

  if X_train.at[num,3]<=10:
    X_train_treated[num,2] = 0
  else: X_train_treated[num,2] = 1
 
  if X_train.at[num,2]<X_train.at[num,3]:
    X_train_treated[num,3] = 0
  else: X_train_treated[num,3] = 1

  if X_train.at[num,0]<=20:
    X_train_treated[num,4] = 0
  else: X_train_treated[num,4] = 1

# expressão de prêmio para indicar probabilidade de maior ou menor prêmio
  delta=0
  delta= ((abs((X_train.at[num,0]-X_train.at[num,4])+(X_train.at[num,2]-X_train.at[num,6]+(X_train.at[num,3]-X_train.at[num,7]))))/3)**2
  #X_train_treated[num,5] = delta
  X_train_treated_prize[num] = delta
  num=num+1

X_train__normalized = preprocessing.normalize(X_train_treated_prize, axis=0)

X_train__normalized=1-X_train__normalized

#train sample
cut_train = int( 0.8 * X_train_len_line)
X_train_cut = np.zeros((cut_train,6), dtype=float)
Y_train_cut = np.zeros((cut_train,4), dtype=float)

#test sample
cut_test = X_train_len_line - cut_train
X_test_cut = np.zeros((cut_test,6), dtype=float)
Y_test_cut = np.zeros((cut_test,4), dtype=float)

#inserindo prêmio
num = 0
while num < X_train_len_line:
  #print (num)
  X_train_treated[num,5] = X_train__normalized[num]
  if num < cut_train:
    X_train_cut [num]= X_train_treated[num]
  else: X_test_cut [num-cut_train]= X_train_treated[num]
  num=num+1

#fim tratamento X_train_cut - file for training

#tratamento Y_train
#+++++++++++++++++++++++
# possibilidade de codificação
set(Y_train)
label_encoder = LabelEncoder()
valores_numericos = label_encoder.fit_transform(Y_train)
#print(valores_numericos)
#set(valores_numericos)
#valor_real = label_encoder.inverse_transform(valores_numericos)
#print(valor_real)
#+++++++++++++++++++++++
indices = valores_numericos
depth = 4
Y_train_tensor=tf.one_hot(valores_numericos, depth, on_value=1.0, off_value=0.0)

num = 0
Y_train_tensor_array = Y_train_tensor
while num < X_train_len_line:

  if num < cut_train:
    Y_train_cut [num]= Y_train_tensor_array[num]
  else: Y_test_cut [num-cut_train]= Y_train_tensor_array[num]
  num=num+1

#resultados finais X_train_cut, X_test_cut, Y_train_cut, Y_test_cut

classifier = Sequential() # Initialising the ANN

classifier.add(Dense(units = 128, activation = 'relu', input_dim = 6))
classifier.add(Dense(units = 384, activation = 'relu'))
classifier.add(Dense(units = 64, activation = 'relu'))
classifier.add(Dense(units = 4, activation = 'softmax'))

classifier.compile(
    loss=tf.keras.losses.categorical_crossentropy,
    optimizer=tf.keras.optimizers.SGD(learning_rate=0.05),
    metrics=[
        tf.keras.metrics.CategoricalAccuracy(name='accuracy'),
        tf.keras.metrics.Precision(name='precision'),
        tf.keras.metrics.Recall(name='recall')
    ])

history = classifier.fit(X_train_cut, Y_train_cut, batch_size = 1, epochs=1250)

rcParams['figure.figsize'] = (18, 8)
rcParams['axes.spines.top'] = False
rcParams['axes.spines.right'] = False
plt.plot(
    np.arange(1, 1251), 
    history.history['loss'], label='Loss'
)
plt.plot(
    np.arange(1, 1251), 
    history.history['accuracy'], label='Accuracy'
)
plt.plot(
    np.arange(1, 1251), 
    history.history['precision'], label='Precision'
)
plt.plot(
    np.arange(1, 1251), 
    history.history['recall'], label='Recall'
)
plt.title('Evaluation metrics', size=20)
plt.xlabel('Epoch', size=14)
plt.legend();

# Save the model
filepath = 'D:/Treinamento/RoboCarro/Rob6'
save_model(classifier, filepath)

ser = serial.Serial(port = 'COM4', baudrate=9600, timeout=1)

print ('Dar reset no robô. Andar (s/n)?')
digitado = input()

print (digitado)

if digitado == 's':
  andar = True
else: andar = False


time.sleep(2)
while andar==True:

  print ('dentro do loop')



#  print(andar)

  
  line = ser.readline()  
  print (line)
  # receber input de sensores e subir entrada no modelo para receber comando de direção
  print('depois line')
  num = 0
  X_input_treated= np.zeros(6, dtype=float)
  X_input= np.zeros(8, dtype=float)
  #exemplo de leitura de sensores para teste sw
  print (X_input_treated)
  #X_input = [49,13,57,36,40,47,47,24]

  line = line.decode('latin-1')
  
  line=line[:-2]
  
  line_s=line.split(',')
  
  X_input[0]=int(line_s[0]) 
  X_input[1]=int(line_s[1])
  X_input[2]=int(line_s[2])
  X_input[3]=int(line_s[3])
  X_input[4]=int(line_s[4]) 
  X_input[5]=int(line_s[5])
  X_input[6]=int(line_s[6])
  X_input[7]=int(line_s[7])
  
 

  print ('X_input is', X_input)
  
  if X_input[1]<=20:

      X_input_treated[0] = 0
  else: X_input_treated[0] = 1

  if X_input[2]<=10:
    X_input_treated[1] = 0
  else: X_input_treated[1] = 1

  if X_input[3]<=10:
    X_input_treated[2] = 0
  else: X_input_treated[2] = 1
 
  if X_input[2]<X_input[3]:
    X_input_treated[3] = 0
  else: X_input_treated[3] = 1

  if X_input[0]<=20:
    X_input_treated[4] = 0
  else: X_input_treated[4] = 1
  
  print (X_input_treated)
 
  # expressão de prêmio para indicar probabilidade de maior ou menor prêmio
  delta=0
  delta= ((abs((X_input[0]-X_input[4])+(X_input[2]-X_input[6]+(X_input[3]-X_input[7]))))/3)**2
  #X_train_treated[num,5] = delta
  X_input_treated_prize = delta

  #Y_input_pred = classifier.predict(X_input__normalized)
  X_train_treated_prize
  X_train_treated_p_len=len(X_train_treated_prize)
  X_input_treated_temp= np.zeros((X_train_treated_p_len+1,1), dtype=float)
  num=0
  while num  <X_train_treated_p_len+1:
    if num<X_train_treated_p_len:
      X_input_treated_temp[num] = X_train_treated_prize[num]
    else: X_input_treated_temp[num] = delta
    num=num+1
  #X_input_treated_temp.reshape(-1, 1)
  X_input__normalized = preprocessing.normalize(X_input_treated_temp,axis=0)
  X_input__normalized=1-X_input__normalized
  X_input_treated[5] = X_input__normalized[X_train_treated_p_len]
  print (X_input_treated)
  X_input_treated_array=np.array(X_input_treated)
  X_input_data= pd.DataFrame(X_input_treated_array)
  newarr = X_input_treated.reshape(1,6)
  print (newarr)
  Y_pred_input = classifier.predict(newarr)

  print ('\nY_pred_input is', Y_pred_input)

  #Y_pred_input
  comando = [b'f', b't', b'e', b'd', b'p']
  if Y_pred_input [0,0]>Y_pred_input [0,1] and Y_pred_input [0,0]>Y_pred_input [0,2] and Y_pred_input [0,0]>Y_pred_input [0,3]:
#    print ('100, frente')
     print ('100, direita')
     disparo = comando[3]
  elif Y_pred_input [0,1]>Y_pred_input [0,0] and Y_pred_input [0,1]>Y_pred_input [0,2] and Y_pred_input [0,1]>Y_pred_input [0,3]:
#    print('101, trás')
    print('101, esquerdq')
    disparo = comando[2]
  elif Y_pred_input [0,2]>Y_pred_input [0,0] and Y_pred_input [0,2]>Y_pred_input [0,1] and Y_pred_input [0,2]>Y_pred_input [0,3]:
    print('102, frente')
    disparo = comando[0]
  elif Y_pred_input [0,3]>Y_pred_input [0,0] and Y_pred_input [0,3]>Y_pred_input [0,1] and Y_pred_input [0,3]>Y_pred_input [0,2]:
    print('116, trás')
    disparo = comando[1]
  else: print('error')

  
 # in_loop=b'i'
  print ('\n disparo is', disparo)
#  ser.write(in_loop)

  ser.write(disparo)
#  in_loop='o' #out do loop
  time.sleep(5)




  
ser.close()