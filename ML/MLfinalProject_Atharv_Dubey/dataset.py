import cv2
import mediapipe as mp
import pandas as pd
import os

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# CSV File to Store Data
csv_filename = "hand_gesture_datasetThumbsUp.csv"

# Define column headers (Each landmark has x, y, and z separate)
columns = []
for i in range(21):
    columns.extend([f"x{i}", f"y{i}", f"z{i}"])
columns.append("gesture")  # Add gesture label at the end

# If CSV does not exist, create it with headers
if not os.path.exists(csv_filename):
    df = pd.DataFrame(columns=columns)
    df.to_csv(csv_filename, index=False)
    print(f"Created new dataset: {csv_filename}")

# Open webcam
cap = cv2.VideoCapture(0)

# Set gesture label (Change this before recording each gesture)
gesture_label = "ThumbsUp"

print("Press 'C' to capture a gesture, 'Q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip and convert to RGB
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract landmark coordinates relative to the wrist
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            landmarks = []

            for lm in hand_landmarks.landmark:
                x, y, z = lm.x - wrist.x, lm.y - wrist.y, lm.z - wrist.z
                landmarks.extend([x, y, z])  # Store x, y, z separately

            # Show text indicating recording instructions
            cv2.putText(frame, "Press 'C' to Capture, 'Q' to Quit", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # Capture data when 'C' is pressed
            if cv2.waitKey(1) & 0xFF == ord('c'):
                landmarks.append(gesture_label)

                # Append to CSV
                df = pd.DataFrame([landmarks], columns=columns)
                df.to_csv(csv_filename, mode='a', header=False, index=False)
                print(f"Captured: {gesture_label}")

    # Show frame
    cv2.imshow("Hand Tracking", frame)

    # Press 'Q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
print("Dataset collection complete.")
