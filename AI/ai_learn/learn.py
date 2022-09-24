import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .utils import preprocess_all_data

all_data = preprocess_all_data(pd.read_csv('data_candidates.csv', sep=';', header=None),
                               pd.read_csv('data_jobs.csv', sep=';', header=None),
                               pd.read_csv('data_candidates_education.csv', sep=';', header=None))

mask = np.random.choice([True, False], size=len(all_data), p=[0.05, 0.95])

training_data = np.asarray(all_data[~mask][all_data.columns[:-1]])
training_labels = np.asarray(all_data[~mask]['status'])
test_data = np.asarray(all_data[mask][all_data.columns[:-1]])
test_labels = np.asarray(all_data[mask]['status'])

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
