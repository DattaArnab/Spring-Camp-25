import cv2
import numpy as np
import mediapipe as mp
import os
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
CSV_FILE = "LeftSwipeDynamic2.csv"
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w") as f:
        f.write(",".join([f"f{i}" for i in range(30 * 63)]) + "\n")  
cap = cv2.VideoCapture(0)

recording = False  
sequence = []
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    landmarks = []
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            wrist = hand_landmarks.landmark[0]  
            
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x - wrist.x, lm.y - wrist.y, lm.z - wrist.z])
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    if recording and len(landmarks) == 63:
        sequence.append(landmarks)
    cv2.putText(frame, "Press 'W' to record 30 frames", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    if recording:
        cv2.putText(frame, "Recording...", (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.imshow("Hand Gesture Recorder", frame)
    key = cv2.waitKey(1)
    if key == ord('w') and not recording:
        print("Recording started...")
        recording = True
        sequence = [] 
    if recording and len(sequence) == 30:
        flat_sequence = np.array(sequence).flatten()
        with open(CSV_FILE, "a") as f:
            f.write(",".join(map(str, flat_sequence)) + "\n")
        recording = False  
    if key == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
