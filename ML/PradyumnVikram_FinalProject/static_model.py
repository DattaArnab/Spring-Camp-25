import pandas as pd
import tensorboard as tb
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.utils import shuffle


df = pd.read_csv('static_data.csv')
df = shuffle(df).reset_index(drop=True)

design_matrix = df.iloc[:, :63].values
target_vector = df.iloc[:, 63].values

target_vector = tf.keras.utils.to_categorical(target_vector, num_classes=4)

X_train, X_test, y_train, y_test = train_test_split(design_matrix, target_vector, test_size=0.2, random_state=42)

model = Sequential([
    Dense(128, activation='relu', input_shape=(63,)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(32, activation='relu'),
    Dense(4, activation='softmax') 
])

model.compile(optimizer=Adam(learning_rate=0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train, y_train,
                    epochs=100,
                    batch_size=32,
                    validation_split=0.2,
                    verbose=1)

test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test accuracy: {test_accuracy:}")

model.save('static_gesture_classifier.h5')


