import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
from collections import deque

static_model = tf.keras.models.load_model("Static\staticGestureANN5.keras")  
dynamic_model = tf.keras.models.load_model("Dynamic2\DynamicModel21.keras")  
STATIC_GESTURES =  {0: "Fist", 1: "OpenPalm", 2: "Peace", 3:"ThumbsUp", 4:"Thumbs Down"}  
DYNAMIC_GESTURES = {0: "Wave", 1: "Hello"} 
mp_hands = mp.solutions.hands
mp_draw= mp.solutions.drawing_utils
hands =mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)
cap = cv2.VideoCapture(0)
prev_landmarks = None
movement_threshold = 0.038  # Found by Experimenting different values
frame_buffer = deque(maxlen=30)  
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    rgb_frame =cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            wrist=hand_landmarks.landmark[0]
            landmarks=np.array([[lm.x - wrist.x, lm.y - wrist.y, lm.z - wrist.z] for lm in hand_landmarks.landmark])
            input_data=landmarks.flatten().reshape(1, 63)
            # Detect Movement
            if prev_landmarks is not None:
                movement = np.linalg.norm(landmarks-prev_landmarks)
                if movement > movement_threshold:
                    is_moving = True
                else:
                    is_moving = False
            else:
                is_moving =False
            prev_landmarks= landmarks.copy()
            #static
            if not is_moving:
                prediction= static_model.predict(input_data)
                label_index =np.argmax(prediction)
                label = STATIC_GESTURES.get(label_index,"Unknown")
                cv2.putText(frame, f"Static: {label}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            #dynamic
            if is_moving:
                frame_buffer.append(landmarks.flatten())  # Collect 30 frames
                if len(frame_buffer)==30:
                    dynamic_input=np.array(frame_buffer).reshape(1,30,63)
        
                    prediction=dynamic_model.predict(dynamic_input)  
                predicted_label=int(prediction[0][0]>0.5)
                print("Raw Prediction:",predicted_label)
                label = DYNAMIC_GESTURES.get(predicted_label,"Unknown")
                if predicted_label==0:
                    cv2.putText(frame, "Dynamic: Wave", (50,100), cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
                elif predicted_label==1:
                    cv2.putText(frame, "Dynamic: Hello", (50, 100), cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2)
    else:
        cv2.putText(frame,"No Hand Detected",(50, 50),cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2)

    cv2.imshow("Hand Gesture Recognition",frame)

    if cv2.waitKey(1)&0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()