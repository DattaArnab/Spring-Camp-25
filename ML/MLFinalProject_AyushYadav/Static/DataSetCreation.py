import cv2
import mediapipe as mp
import csv
import os
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils
csv_file = "test.csv"
if not os.path.exists(csv_file):
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        header = [item for i in range(1, 22) for item in (f"x{i}", f"y{i}", f"z{i}")]
        writer.writerow(header)
cap = cv2.VideoCapture(0)
data = []
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            wrist = hand_landmarks.landmark[0]
            wrist_x, wrist_y, wrist_z = wrist.x, wrist.y, wrist.z
            key = cv2.waitKey(1) & 0xFF
            if key == ord('w'):
                relative_landmarks = []
                for i, lm in enumerate(hand_landmarks.landmark):
                    rel_x = lm.x - wrist_x
                    rel_y = lm.y - wrist_y
                    rel_z = lm.z - wrist_z
                    relative_landmarks.extend([rel_x, rel_y, rel_z])
                data.append(relative_landmarks)
    cv2.imshow("Hand Gesture Recording", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
with open(csv_file, "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(data)