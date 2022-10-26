# -*- coding: utf-8 -*-
"""app.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Odb7EUC13Zoun70j791fZPFUnqvqm2Pu
"""

import cv2
import numpy as np
import streamlit as st
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2,preprocess_input as mobilenet_v2_preprocess_input
from skimage import segmentation
import matplotlib.pyplot as plt; plt.rcParams.update({'font.family':'serif'})
from tensorflow.keras import backend as keras

def dice_coef(y_true, y_pred):
    y_true_f = keras.flatten(y_true)
    y_pred_f = keras.flatten(y_pred)
    intersection = keras.sum(y_true_f * y_pred_f)
    return (2. * intersection + 1) / (keras.sum(y_true_f) + keras.sum(y_pred_f) + 1)

def imag(resized,edges):
  plt.imshow(resized, cmap='gray')
  plt.contour(edges,[0.5],colors = ['red'])
  ax = plt.gca()
  ax.axes.xaxis.set_ticks([])
  ax.axes.yaxis.set_ticks([])
  plt.savefig('prediction.png')
  return plt.imread('/content/prediction.png')
  


model_path = '/content/model_seg.h5'

model = tf.keras.models.load_model(model_path,custom_objects={'dice_coef':dice_coef})

uploaded_file = st.file_uploader("Choose an image file") #, type="jpg")

if uploaded_file is not None:
    # Convert the file to an opencv image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)      # Generar la imagen que se entregó en la interfaz.
    opencv_image = cv2.imdecode(file_bytes, 1)                                    # Generar la imagen que se entregó en la interfaz.
    resized = cv2.resize(opencv_image,(256,256))
    # Now do something with the image! For example, let's display it:
    st.image(opencv_image, channels="RGB")

    # resized = mobilenet_v2_preprocess_input(resized)
    img_reshape = resized[np.newaxis,...]

    Genrate_pred = st.button("Generate Prediction")    
    if Genrate_pred:
        prediction = model.predict(img_reshape)
        prediction[prediction > 0.5] = 1
        prediction[prediction <= 0.5] = 0

        edges = segmentation.clear_border( np.squeeze(prediction))
        # plt.contour(Predi_unet,[0.5], colors = ['yellow'])

        final_image = imag(resized,edges)

        st.title("Predicted Label for the image is")
        st.image(final_image, caption='Enter any caption here')