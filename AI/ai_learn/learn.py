import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

training_data = []#вход
training_labels = []#выход
test_data = []#вход
test_labels = []#выход

model = tf.keras.Sequential([
    tf.keras.layers.Dense(6, activation=tf.nn.relu, input_shape=(32, )),
    tf.keras.layers.Dense(2, activation=tf.nn.softmax)
])


model.compile(optimizer = tf.keras.optimizers.Adam(),
              loss = 'binary_crossentropy',
              metrics=['accuracy'])
model.summary()

history = model.fit(training_data, training_labels, epochs=50)
model.evaluate(test_data, test_labels)

predictions = model.predict([[0.3, 1 , 0.1, 0.03, 1, 0.1, 0, 0, 0.004 ]]) # test
print(history.history.keys())

np.set_printoptions(suppress=True)
plt.plot(history.history['accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()