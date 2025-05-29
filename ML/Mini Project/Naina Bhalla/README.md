# Mini-Project: Hand Gesture Recognition
### Naina Bhalla

## Overview<br>
The project implements two different models for static and dynamic hand gesture classification. The static model is a NN while the dynamic model is 2D-CNN+LSTM. The final result is shown using cv2 on the webcam-feed.

## Dataset<br>
The static dataset contains 7 classes [one,peace,three,not in dataset,thumbs_up,thumps_down,palm] each with 300 images except "not in dataset" with 500 images of other random gestures. The dyanmic dataset contains of video-frames of 4 classes[wave,clap,no,hand wave] in form of numpy arrays.

## Static Classification<br>
The static model is a neural network trained on the 21 landmarks acquired by mediapipe.<br>

### Model Architecture<br>
![image](https://github.com/user-attachments/assets/4ef00753-753a-4e59-ba11-1cdecfae87e2)


### Accuracy<br>
This achieves test loss of 0.2819 and test accuracy of 93.26%<br>
![image](https://github.com/user-attachments/assets/76a22ef7-fb34-4f4a-ac9e-d7b92f838901)


## Dynamic Classification<br>
This model is a CNN+LSTM model with TimeDistributed that is used to apply convolutional layers to each video frame independently for sequential learning of the model.<br>

### Model Architecture<br>
![image](https://github.com/user-attachments/assets/c4b8cd06-fd14-49c2-9870-8d5143ea7695)<br>

## Final results
The last cell runs a code to open the webcam feed. It then sends the frames accordingly to the models whether they are static or dynamic. It shows the predicted gesture for both the hands.
