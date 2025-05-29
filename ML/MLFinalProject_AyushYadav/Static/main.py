import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
model = tf.keras.models.load_model("Static\staticGestureANN5.keras")
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
gesture_labels = {0: "Fist", 1: "OpenPalm", 2: "Peace", 3:"ThumbsUp", 4:"Thumbs Down"}  
cap = cv2.VideoCapture(0) 
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break    
    frame = cv2.flip(frame, 1) 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
    results= hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS) 
            landmarks= hand_landmarks.landmark
            wrist =landmarks[0]  
            coords= []
            for i in range(21): 
                x_rel=landmarks[i].x - wrist.x 
                y_rel=landmarks[i].y - wrist.y 
                z_rel=landmarks[i].z - wrist.z 
                coords.extend([x_rel, y_rel,z_rel])
            input_data=np.array(coords).reshape(1, -1)
            prediction=model.predict(input_data)
            predicted_label=np.argmax(prediction)
            gesture_name =gesture_labels.get(predicted_label, "Unknown")
            cv2.putText(frame, f"Gesture: {gesture_name}", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Hand Gesture Recognition", frame)
    if cv2.waitKey(1)&0xFF==ord("q"):
        break
cap.release()
cv2.destroyAllWindows()