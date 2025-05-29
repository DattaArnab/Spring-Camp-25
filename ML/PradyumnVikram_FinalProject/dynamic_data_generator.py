import cv2
import mediapipe as mp
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def normalise_wrt_wrist(landmarks):
    wrist = landmarks[0]
    return [landmark - wrist for landmark in landmarks]

cap = cv2.VideoCapture(0)

data = []
sequence_length = 20

for class_ in range(3):
    i=0
    print('now collecting data for', class_)
    input('press enter to continue')
    while i<200:
        ret, frame = cap.read()
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)
        if results.multi_hand_landmarks:
            i+=1
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = [np.array([lm.x, lm.y, lm.z]) for lm in hand_landmarks.landmark]
                normalised_hand_landmarks = normalise_wrt_wrist(landmarks)
                feature = [coord for coordinates in normalised_hand_landmarks for coord in coordinates]
                feature.append(class_)
                data.append(feature)

                mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0,0,255), thickness=2))
        cv2.imshow('Live Feed', frame)
        if cv2.waitKey(1) == ord('q'):
            break

features = [row[:63] for row in data]
target_vec = [row[63] for row in data]

sequences = []
sequence_targets = []

for i in range(len(features)-sequence_length+1):
    seq = features[i:i+sequence_length]
    sequences.append(seq)
    sequence_targets.append(target_vec[i+sequence_length-1])
    
design_matrix = np.array(sequences)
targets = sequence_targets

csv_data = []

for i in range(len(design_matrix)):
    flattened = design_matrix[i].flatten()
    csv_data.append(np.append(flattened, targets[i]))

csv_data = np.array(csv_data)

df = pd.DataFrame(csv_data, columns=[i for i in range(63*sequence_length+1)])
df.to_csv('dynamic_data.csv', index=False)
cap.release()
cv2.destroyAllWindows()