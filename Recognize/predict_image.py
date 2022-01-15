import tensorflow as tf
import cv2
import numpy as np
import matplotlib.pyplot as plt

class predict_image:
    result = 0
    def __init__(self, root):
        new_model = tf.keras.models.load_model('recog/model_and_weight_12_12/model_.h5')
        new_model.load_weights("recog/model_and_weight_12_12/model_weights_.h5")
        image = cv2.imread(root,cv2.IMREAD_GRAYSCALE)
        # print("Hello world")
        # print(image.shape)
        plt.imshow(image.reshape(28,28), cmap='gray')
        y_predict = new_model.predict(image.reshape(1,28,28,1))
        self.result = np.argmax(y_predict)

# class predict_array:
#     result = 0
#     def __init__(self, root):
#         new_model = tf.keras.models.load_model('recog/model_and_weight_12_12/model_.h5')
#         new_model.load_weights("recog/model_and_weight_12_12/model_weights_.h5")
#         image = root
#         print(image)
#         plt.imshow(image.reshape(28,28), cmap='gray')
#         y_predict = new_model.predict(image.reshape(1,28,28,1))
#         self.result = np.argmax(y_predict)




# def predict_from_image(root):
#     new_model = tf.keras.models.load_model('recog/model_and_weight_12_12/model_.h5')
#     new_model.load_weights("recog/model_and_weight_12_12/model_weights_.h5")
#     image = cv2.imread(root,cv2.IMREAD_GRAYSCALE)
#     print(image)
#     plt.imshow(image.reshape(28,28), cmap='gray')
#     y_predict = new_model.predict(image.reshape(1,28,28,1))
#     return np.argmax(y_predict)   


# def predict_from_array(nparray):
#     new_model = tf.keras.models.load_model('recog/model_and_weight_12_12/model_.h5')
#     new_model.load_weights("recog/model_and_weight_12_12/model_weights_.h5")
#     plt.imshow(np.array.reshape(28,28), cmap='gray')
#     y_predict = new_model.predict(np.array.reshape(1,28,28,1))
#     return np.argmax(y_predict)  




# load model and weight

# new_model = tf.keras.models.load_model('/content/drive/MyDrive/model.h5')
# new_model.load_weights("/content/drive/MyDrive/model_weights.h5")

# new_model = tf.keras.models.load_model('word-recog/model_and_weight_12_12/model_.h5')
# new_model.load_weights("word-recog/model_and_weight_12_12/model_weights_.h5")
# image = cv2.imread("word-recog/image/U.png",cv2.IMREAD_GRAYSCALE)
# plt.imshow(image.reshape(28,28), cmap='gray')
# y_predict = new_model.predict(image.reshape(1,28,28,1))
# print('Giá trị dự đoán: ', np.argmax(y_predict))

