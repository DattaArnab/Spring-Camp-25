import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from collections import deque
model =tf.keras.models.load_model("Dynamic2\DynamicModel21.keras")
mp_hands= mp.solutions.hands
mp_drawing= mp.solutions.drawing_utils
hands= mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
cap= cv2.VideoCapture(0)
sequence =deque(maxlen=30) 
previous_landmarks = None 
movement_threshold = 0.038  
while cap.isOpened():
    ret,frame= cap.read()
    if not ret:
        break
    frame =cv2.flip(frame, 1)
    rgb_frame= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results=hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            wrist = hand_landmarks.landmark[0]  
            landmarks = []
            for i in range(21):
                x =hand_landmarks.landmark[i].x-wrist.x
                y= hand_landmarks.landmark[i].y-wrist.y
                z = hand_landmarks.landmark[i].z-wrist.z
                landmarks.extend([x, y, z])

            if previous_landmarks is not None:
                movement = np.linalg.norm(np.array(landmarks) - np.array(previous_landmarks))
                if movement < movement_threshold:
                    cv2.putText(frame, "Static", (50, 50),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                    cv2.imshow("Hand Gesture Recognition", frame)
                    continue 
            previous_landmarks = landmarks
            sequence.append(landmarks)
            if len(sequence) == 30:
                input_data = np.expand_dims(np.array(sequence), axis=0)
                prediction = model.predict(input_data)
                predicted_label = int(prediction > 0.5)
                gesture_text = "Hello" if predicted_label == 1 else "Wave"
                cv2.putText(frame, f"Gesture: {gesture_text}", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    else:
        previous_landmarks = None
    cv2.imshow("Hand Gesture Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()