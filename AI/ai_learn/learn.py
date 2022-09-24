import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import preprocess_all_data
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))


all_data = preprocess_all_data(pd.read_csv(dir_path+'\data_candidates.csv', sep=';', header=None),
                               pd.read_csv(dir_path+'\data_jobs.csv', sep=';', header=None),
                               pd.read_csv(dir_path+'\data_candidates_education.csv', sep=';', header=None),
                               pd.read_csv(dir_path+'\data_candidates_work_places.csv', sep=';', header=None))

mask = np.random.choice([True, False], size=len(all_data), p=[0.05, 0.95])

training_data = np.asarray(all_data[~mask][all_data.columns[:-1]])
training_labels = np.asarray(all_data[~mask]['status'])
test_data = np.asarray(all_data[mask][all_data.columns[:-1]])
test_labels = np.asarray(all_data[mask]['status'])

model = tf.keras.Sequential([
    tf.keras.layers.Dense(34, activation=tf.nn.relu, input_shape=(34, )),
    tf.keras.layers.Dense(16, activation=tf.nn.relu),
    tf.keras.layers.Dense(1, activation=tf.nn.relu)
])


model.compile(optimizer = tf.keras.optimizers.Adam(),
              loss = 'mse',
              metrics=['accuracy'])
model.summary()

history = model.fit(training_data, training_labels, epochs=25, validation_split=0.1)
model.evaluate(test_data, test_labels)

# predictions = model.predict([[0.3, 1 , 0.1, 0.03, 1, 0.1, 0, 0, 0.004 ]])
# print(history.history.keys())

np.set_printoptions(suppress=True)
plt.plot(history.history['accuracy', 'val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
