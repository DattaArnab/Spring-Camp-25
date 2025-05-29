The task was to create a gesture recognizer. 

I have used MediaPipe for gesture recognition. MediaPipe Hand Tracking detects 21 key landmark points on each hand, covering the fingertips, joints, and palm. These landmarks are used to analyze hand poses and gestures by mapping their relative positions and movements in 3D space. 

The challenge was that the gesture could be either static or dynamic. 
To achieve this distinciton I have used a simple metric that tracks "movement". It is the mean of the difference between landmarks of the current and the previous set of points. If movement is greater than a treshold, it is classifeid as dynamic. 

I have also recorded my own gestures for the input data in order to train the models.

For Static Gestures I have used 1DConv and for Dynamic Gestures I have used an LSTM. 

Static Gestures are "FIST", "PEACE" and a mystery gesture for you to find out ;). 
Dynamic Gestures are "BYE" and "WAVE".
