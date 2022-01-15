from typing import List
import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt

class predict_array:
    FResult = ''
    predict = 0
    def __init__(self, Listroot, new_model):
        self.FResult = ''
        # new_model = tf.keras.models.load_model('Word_recognize/model_and_weight_12_12/model_.h5')
        # new_model.load_weights("Word_recognize/model_and_weight_12_12/model_weights_.h5")
        dict = {0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z',26:'0',27:'1',28:'2', 29:'3', 30:'4',31:'5',32:'6', 33:'7', 34:'8', 35:'9'} 
        for i in range(0, len(Listroot), 1):
            # plt.imshow(Listroot[i].reshape(28,28), cmap='gray')
            self.y_predict = new_model.predict(Listroot[i].reshape(1,28,28,1))
            # print(new_model.predict(Listroot[i].reshape(1,28,28,1)))
            result = np.argmax(self.y_predict)
            self.FResult += dict[result]



