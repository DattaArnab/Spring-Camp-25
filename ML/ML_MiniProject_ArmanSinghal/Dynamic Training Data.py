import cv2
import mediapipe as mp
import numpy as np

def CreateDynamicTrainingData(label):

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    mp_draw = mp.solutions.drawing_utils
    datapoints = []
    keypoints_history = []

    cap = cv2.VideoCapture(0)

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                keypoints = [[lmk.x, lmk.y] for lmk in hand_landmarks.landmark]
                keypoints_history.append(keypoints)
                
                if cv2.waitKey(1) & 0xFF == ord('c'):
                    datapoints.append(keypoints_history[-30:])
                    print(f"Data Points Captured: {len(datapoints)}")
                    keypoints_history = []

                if cv2.waitKey(1) & 0xFF == ord('s'):
                    data = np.array(datapoints)
                    print(data.shape)
                    np.save(f"Data\Dynamic\Dynamic - {label}", data)
                    print("Training Data Saved")
                    break

        cv2.imshow("Hand Sign Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    label = input("Enter the label for the training data: ")
    CreateDynamicTrainingData(label)