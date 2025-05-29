import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam

df = pd.read_csv('dynamic_data.csv')

design_matrix = df.iloc[:, :-1].values
target_vector = df.iloc[:, -1].values

sequence_length = 20  
num_features = 63
X = X.reshape(-1, sequence_length, num_features)



X_train, X_test, y_train, y_test = train_test_split(design_matrix, target_vector, test_size=0.2, random_state=42)


model = Sequential([
    LSTM(64, input_shape=(sequence_length, num_features), return_sequences=True),
    Dropout(0.3),
    LSTM(32),
    Dropout(0.3),
    Dense(16, activation='relu'),
    Dense(3, activation='softmax')  
])


model.compile(optimizer=Adam(learning_rate=0.001),
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])


history = model.fit(X_train, y_train, 
                    epochs=50, 
                    batch_size=32, 
                    validation_split=0.2,
                    verbose=1)


test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test accuracy: {test_accuracy}")

model.save('dynamic_gesture_classifier.h5')
