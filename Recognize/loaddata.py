# -*- coding: utf-8 -*-

from keras.datasets import mnist
import pandas as pd 
import numpy as np
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

def load_data():
  (X_train_1, y_train_1), (X_test_1, y_test_1) = mnist.load_data()
  
  X_dataset_1 = np.concatenate((X_train_1,X_test_1), axis = 0)
  y_dataset_1 = np.concatenate((y_train_1,y_test_1), axis = 0)
  
  # A-Z : 0 : 25 , 0-9 : 26-35 
  for i in range(len(y_dataset_1)):
    y_dataset_1[i] = y_dataset_1[i] + 26
  
  X_dataset_1 = X_dataset_1.reshape((70000, 784))
  y_dataset_1 = y_dataset_1.reshape((70000, 1))
  mnist_dataset = np.concatenate((y_dataset_1, X_dataset_1), axis = 1)

  dataset = pd.read_csv("/content/drive/MyDrive/Deep Learning/A_Z Handwritten Data.csv").astype('float32')
  dataset.rename(columns={'0':'label'}, inplace=True)
  kaggle_dataset = dataset.to_numpy()

  # print(kaggle_dataset.shape)
  # print(mnist_dataset.shape)

  dataset = np.concatenate((kaggle_dataset, mnist_dataset), axis = 0)
  # print(dataset.shape)
  dataset_pd = pd.DataFrame(dataset, columns = [x for x in range(785)])
  dataset_pd = shuffle(dataset_pd)
  dataset_pd.rename(columns={0:'label'}, inplace=True)

  X = dataset_pd.drop('label',axis = 1)
  y = dataset_pd['label']

  data = X.to_numpy()
  label = y.to_numpy()

  plt.imshow(data[9990].reshape(28,28))
  print(label[9990])

  # vẽ biểu đồ xem số lượng mẫu mỗi loại
  alphabets_mapper = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V'
  ,22:'W',23:'X',24:'Y',25:'Z',26:'0',27:'1',28:'2', 29:'3', 30:'4',31:'5',32:'6', 33:'7', 34:'8', 35:'9'} 
  dataset_alphabets = dataset_pd.copy()
  dataset_pd['label'] = dataset_pd['label'].map(alphabets_mapper)
  label_size = dataset_pd.groupby('label').size()
  label_size.plot.barh(figsize=(10,10))

  # chia tập dữ liệu ra thành 3 tập là train, test, validate theo tỉ lệ 7:1.5:1.5 
  SIZE = data.shape[0]
  X_train,y_train = data[0:int(0.7*SIZE)], label[0:int(0.7*SIZE)]
  X_test, y_test = data[int(0.7*SIZE):int(0.85*SIZE)], label[int(0.7*SIZE):int(0.85*SIZE)]
  X_val, y_val = data[int(0.85*SIZE):SIZE], label[int(0.85*SIZE): SIZE]

  # print(X_train.shape)
  # print(X_test.shape)
  # print(X_val.shape)
  return ((X_train, y_train),(X_test, y_test),(X_val,y_val))