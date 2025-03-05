# Hand Gesture Recognition Project

## Overview

This project recognizes hand gestures from video sequences using a PyTorch BiLSTM model. It includes data loading, preprocessing with MediaPipe hand landmarks, model training, and validation. Multi-GPU support is implemented for faster training on platforms like Kaggle.

## Key Components

-   **`hand_gesture_config.json`**: JSON configuration file containing hyperparameters, class names, and paths.
-   **`train.csv`**: CSV file with training data information (folder, gesture, label), using semicolon (`;`) as delimiter.
-   **`val.csv`**: CSV file with validation data information (folder, gesture, label), using semicolon (`;`) as delimiter.
-   **`HandGestureDataset`**: PyTorch Dataset class for loading and preprocessing data, including MediaPipe landmark extraction.
-   **`BiLSTMModel`**: Bidirectional LSTM model for gesture classification.
-   **Training Loop**: Training and validation functions, including multi-GPU support and learning rate scheduling.
-   **Visualization**: Training history plots and confusion matrices for model evaluation.

## How to Run

1.  Install dependencies: `pip install torch numpy pandas scikit-learn matplotlib seaborn Pillow opencv-python mediapipe tqdm`
2.  Download dataset and place in `/kaggle/input/handgesture/Project_data/`.

dataset link: https://www.kaggle.com/datasets/arnab06/hand-gesture

3.  Run the training script.

## Notes

-   Edit `hand_gesture_config.json` to adjust hyperparameters.
-   Ensure CSV files (`train.csv`, `val.csv`) use semicolon (`;`) as the delimiter.
-   Model checkpoints are saved as `hand_gesture_model.pth`.

4. Run the Inference Script
