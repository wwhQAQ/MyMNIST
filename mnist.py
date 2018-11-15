import keras
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Activation, Dropout, Flatten
from keras.callbacks import ModelCheckpoint
from keras.models import Sequential
from keras.utils import np_utils
import tensorflow as tf
from sklearn.model_selection import train_test_split

import numpy as np
from PIL import Image
import os

image_list = []
label_list = []

train_path = "data/trainingSet"
test_path = "data/testSet"

for label in os.listdir(train_path):
  dir = train_path + "/" + label
  for filename in os.listdir(dir):
    label_list.append(label)
    image_path = dir + "/" + filename
    image = np.array(Image.open(image_path).resize((28,28)))
    image_list.append(image/255.)

image_list = np.array(image_list)
label_list = np.array(label_list)
label_list = np_utils.to_categorical(label_list)

(train_data, test_data, train_label, test_label) = train_test_split(image_list, label_list, test_size=0.3, random_state=111)
train_data = train_data.reshape(-1, 28, 28, 1)
test_data = test_data.reshape(-1, 28, 28, 1)

batch_size = 128
epochs = 5
kernel_size = (4,4)
input_shape = train_data[0].shape

model = Sequential()

model.add(Conv2D(filters=32, kernel_size=kernel_size, input_shape=input_shape, activation="relu"))
model.add(Conv2D(filters=64, kernel_size=kernel_size, activation="relu"))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.2))
model.add(Conv2D(filters=64, kernel_size=kernel_size, activation="relu"))
model.add(Conv2D(filters=64, kernel_size=kernel_size, activation="relu"))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))
model.add(Dense(64, activation="relu"))
model.add(Flatten())
model.add(Dense(10, activation="softmax"))
model.summary()

checkpointer = ModelCheckpoint(filepath = 'sample_mnist.hdf5', verbose=1, save_best_only=True, monitor='val_acc', mode='max')

model.compile(
    optimizer='adadelta',
    loss='categorical_crossentropy',
    metrics=['categorical_accuracy']
)

model.fit(train_data, train_label, batch_size=batch_size, epochs=epochs)

scores = model.evaluate(test_data, test_label, verbose=1)

json_string = model.to_json()
open('mnist.json', 'w').write(json_string)
model.save_weights('mnist.h5')

print('Test loss:', scores[0])
print('Test accuracy:', scores[1])
