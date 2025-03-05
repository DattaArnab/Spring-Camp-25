import cv2
import torch
import numpy as np
import mediapipe as mp
from collections import deque
import json
import time

# Load configuration
with open('config.json', 'r') as f:
    config = json.load(f)

class GestureRecognizer:
    def __init__(self, model_path, config):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.config = config
        self.class_names = config['data_config']['class_names']
        self.sequence_length = config['data_config']['sequence_length']
        self.input_size = tuple(config['data_config']['input_size'])
        
        # Initialize MediaPipe
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        
        # Initialize model
        self.model = self.load_model(model_path)
        self.model.eval()
        
        # Initialize frame buffer
        self.frame_buffer = deque(maxlen=self.sequence_length)
        
        # Motion detection parameters
        self.motion_threshold = 1000
        self.motion_buffer_size = 10
        self.motion_frame_buffer = []
        
    def load_model(self, model_path):
        model = GestureRecognitionModel(self.config).to(self.device)
        checkpoint = torch.load(model_path, map_location=self.device)
        model.load_state_dict(checkpoint['model_state_dict'])
        return model
    
    def preprocess_frame(self, frame):
        frame = cv2.resize(frame, self.input_size)
        results = self.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        landmarks = np.zeros(21 * 3)
        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            landmarks = np.array([[lm.x, lm.y, lm.z] for lm in hand.landmark]).flatten()
            self.mp_drawing.draw_landmarks(frame, hand, self.mp_hands.HAND_CONNECTIONS)
        
        return frame, landmarks
    
    def predict(self):
        if len(self.frame_buffer) < self.sequence_length:
            return None, None
        
        sequence = np.array(list(self.frame_buffer))
        sequence_tensor = torch.FloatTensor(sequence).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            output = self.model(sequence_tensor)
            probabilities = torch.softmax(output, dim=1)
            pred_prob, pred_class = torch.max(probabilities, dim=1)
            
        return self.class_names[pred_class.item()], pred_prob.item()
    
    def calculate_motion(self, frame1, frame2):
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(gray1, gray2)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        motion_score = np.sum(thresh) / 255
        return motion_score
    
    def run_inference(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            raise IOError("Cannot open webcam")
        
        prev_time = 0
        
        # Get the original frame size
        ret, frame = cap.read()
        if not ret:
            raise IOError("Cannot read from webcam")
        original_height, original_width = frame.shape[:2]
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                current_time = time.time()
                fps = 1 / (current_time - prev_time)
                prev_time = current_time
                
                display_frame, landmarks = self.preprocess_frame(frame)
                self.frame_buffer.append(landmarks)
                
                # Motion detection
                self.motion_frame_buffer.append(frame.copy())
                if len(self.motion_frame_buffer) > self.motion_buffer_size:
                    self.motion_frame_buffer.pop(0)
                
                motion_type = "Unknown"
                motion_confidence = 0
                
                if len(self.motion_frame_buffer) >= 2:
                    motion_score = self.calculate_motion(
                        self.motion_frame_buffer[-2], 
                        self.motion_frame_buffer[-1]
                    )
                    motion_type = "Dynamic" if motion_score > self.motion_threshold else "Static"
                    motion_confidence = min(motion_score / self.motion_threshold, 1.0) if motion_type == "Dynamic" \
                                else 1.0 - (motion_score / self.motion_threshold)
                
                # Gesture recognition
                gesture = None
                confidence = 0
                if len(self.frame_buffer) == self.sequence_length:
                    gesture, confidence = self.predict()
                
                # Rescale the frame back to original size
                display_frame = cv2.resize(display_frame, (original_width, original_height))
                
                # Add text to the resized frame
                if gesture and confidence > 0.7:
                    cv2.putText(display_frame, f"{gesture}", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    cv2.putText(display_frame, f"{confidence:.2f}", (10, 70),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.putText(display_frame, f"{motion_type}", (10, 110),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.putText(display_frame, f"FPS: {fps:.2f}", (10, 190),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                cv2.imshow('Gesture Recognition', display_frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                
        finally:
            cap.release()
            cv2.destroyAllWindows()
            self.hands.close()


class GestureRecognitionModel(torch.nn.Module):
    def __init__(self, config):
        super().__init__()
        self.lstm = torch.nn.LSTM(
            input_size=21 * 3,
            hidden_size=config['model_config']['lstm_hidden_size'],
            num_layers=config['model_config']['num_layers'],
            bidirectional=config['model_config']['bidirectional'],
            dropout=config['model_config']['dropout'] if config['model_config']['num_layers'] > 1 else 0,
            batch_first=True
        )
        
        lstm_output_size = (config['model_config']['lstm_hidden_size'] * 
                          (2 if config['model_config']['bidirectional'] else 1))
        
        self.fc = torch.nn.Linear(lstm_output_size, config['model_config']['num_classes'])

    def forward(self, x):
        lstm_out, _ = self.lstm(x)
        return self.fc(lstm_out[:, -1, :])

if __name__ == "__main__":
    model_path = "best_model.pth"
    recognizer = GestureRecognizer(model_path, config)
    recognizer.run_inference()
