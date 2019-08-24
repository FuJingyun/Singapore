import sys
import cv2
import numpy as np
import tensorflow as tf
import keras.backend as K
import glob

from net import simpleconv3
from PIL import Image
from keras.preprocessing.image import img_to_array
from keras.applications.imagenet_utils import preprocess_input

image_size = (500, 500)
batch_shape = (1, ) + image_size + (3, )
# model_path = sys.argv[1]
model_path = './models/model.h5'

config = tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True))
session = tf.Session(config=config)
K.set_session(session)

model = simpleconv3()
model.load_weights(model_path, by_name=True)
model.summary()

file_path='./data/test/'
f_names= glob.glob(file_path+'*.jpg')
#for image_path in f_names:
#    images = Image.open(image_path)

for i in range(len(f_names)):
    images = Image.open('./data/test/'+str(i+1)+'.jpg')
    img = img_to_array(images)
    img = cv2.resize(img, image_size)
    img = np.expand_dims(img, axis=0)
    img = preprocess_input(img)
    result = model.predict(img, batch_size=1)
    print(result)
