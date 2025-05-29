import cv2
import mediapipe as mp
import matplotlib.pyplot as plt 
from tensorflow.keras.models import load_model
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
static_classes = ['Thumbs Up', 'Thumbs Down', 'Ok', 'Stop']
dynamic_classes = ['No No No', 'Hello!', 'Wrist Stretch']
static_model = load_model('static_gesture_classifier.h5')
dynamic_model = load_model('dynamic_gesture_classifier.h5')

sequence_length = 20
input_seq = []
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def frame_difference(frame1, frame2, motion_threshold):
    if len(frame1.shape) == 3:
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    if len(frame2.shape) == 3:
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(frame1, frame2)
    _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
    return cv2.countNonZero(thresh) > motion_threshold


def normalise_wrt_wrist(landmarks):
    wrist = landmarks[0]
    return [landmark - wrist for landmark in landmarks]

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera not functioning")
    exit()
static = True
prev_frame = None
started=0

while True:
    if started:
        prev_frame = frame
    started += 1
    ret, frame = cap.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        if started>0:
            if frame_difference(prev_frame, frame, 7500):
                static = False
            else:
                static=True
        for hand_landmarks in results.multi_hand_landmarks:
            to_write = "None"
            if static:
                landmarks = [np.array([lm.x, lm.y, lm.z]) for lm in hand_landmarks.landmark]
                normalised_hand_landmarks = normalise_wrt_wrist(landmarks)
                feature = np.array([coord for coordinates in normalised_hand_landmarks for coord in coordinates]).reshape(1, 63)
                prediction = static_model.predict([feature])
                to_write = static_classes[prediction.argmax()]
            else:
                landmarks = [np.array([lm.x, lm.y, lm.z]) for lm in hand_landmarks.landmark]
                normalised_hand_landmarks = normalise_wrt_wrist(landmarks)
                feature = np.array([coord for coordinates in normalised_hand_landmarks for coord in coordinates]).reshape(1, 63)

                input_seq.append(feature)

                if len(input_seq)==(sequence_length):
                    to_predict = np.array(input_seq).reshape(1, sequence_length, 63)

                    prediction = dynamic_model.predict(to_predict)
                    to_write = dynamic_classes[prediction.argmax()]
                    print(to_write)
                    input_seq.pop(0)


            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(0,0,255), thickness=2))
            x_min = min(lm.x for lm in hand_landmarks.landmark)
            y_min = min(lm.y for lm in hand_landmarks.landmark)
            x_max = max(lm.x for lm in hand_landmarks.landmark)
            y_max = max(lm.y for lm in hand_landmarks.landmark)

            h, w, _ = frame.shape
            x_min, y_min = int(x_min * w), int(y_min * h)
            x_max, y_max = int(x_max * w), int(y_max * h)

            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            text = to_write
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]

            text_x = x_min
            text_y = y_min - 10

            cv2.putText(frame, text, (text_x, text_y), font, font_scale, (0, 255, 0), font_thickness)

    cv2.imshow('Live Feed', frame)
    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()