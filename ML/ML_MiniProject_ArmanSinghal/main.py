import cv2
import mediapipe as mp
import numpy as np
from isStatic import isstatic
from tensorflow.keras.models import load_model
from collections import deque


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils
landmark_history = deque(maxlen=30)
count = 0

static_dic = {0: 'Dislike', 1: 'Fist', 2: 'Five', 3: 'Four', 4: 'Gun', 5: 'Like', 6: 'OK', 7: 'One', 8: 'Three', 9: 'Two'}
static_model = load_model("Models\static_model.keras")

dynamic_dic = {0: 'Come Here', 1: 'No', 2: 'Air Quotes', 3: 'Wave', 4: 'Yes'}
dynamic_model = load_model("Models\dynamic_model.keras")

cap = cv2.VideoCapture(0)

while cap.isOpened():
    count += 1

    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(frame_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            keypoints = [[lmk.x, lmk.y] for lmk in hand_landmarks.landmark]
            landmark_history.append(keypoints)

            if isstatic(landmark_history) and count > 1:
                cv2.putText(frame, "Static", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f'{static_dic[static_model.predict(np.array(keypoints).reshape(-1, 42)).argmax(axis=1)[0]]}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif not isstatic(landmark_history):
                cv2.putText(frame, "Dynamic", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if len(landmark_history) == 30:
                    cv2.putText(frame, f'{dynamic_dic[dynamic_model.predict(np.array(landmark_history).reshape(-1, 30, 42)).argmax(axis=1)[0]]}', (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                count = 0

    cv2.imshow("Hand Sign Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()