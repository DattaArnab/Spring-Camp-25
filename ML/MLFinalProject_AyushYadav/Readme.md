This consists of 2 folders (dynamic2,static) and one mainfinal2.py script ,the final python script is mainfinal2.py which when executed a live camera will open up on computer and will predict the gestures you do from your left hand ,the gestures it can predict are of two kinds dynamic and static <br>

Dynamic gestures :<br>
1.) Hello<br>
2.) Wave (moving hand left-right)<br>

Static gestures:
1.) Thumbs Up<br>
2.) Thumbs Down<br>
3.) Open Palm<br>
4.) Fist (closed palm)<br>
5.) Peace symbol<br>
<br>
Approach for static gesture prediction :<br>
1.) Dataset Creation:<br>
Used mediapipe to extract 21 points on hand and stored the coordinates of all points on hand with respect to the wrist point in an csv file 
stored this data for all the gestures (Static\DataSetCreation.py) dataset creation is done using this script<br>
2.) Model Training :
Trained an neural network on the created csv file (Static\datasetShuffle+Ann.ipynb) (model name is staticGestureANN5)<br>
3.) Integrated the model:<br>
Integrated the model with live camera feed so that model can make live predictions 

Approach for dynamic gesture prediction : <br>
1.) Dataset Creation:Again used mediapipe and found coordinates of all landmarks wrt wrist and then stored coordinates for 30 frames, (Dynamic2\DataCreation.py) This script was used to make the dataset
<br>
2.)Trained a LSTM model for the data and saved the model ( script for LSTM : Dynamic2\DynamicModel.ipynb) (Saved Model : Dynamic2\DynamicModel21.keras)
<br>
3.) Integrated the model again with live camera feed so that our model can make live predictions 


At last combined both static and dynamic model together to make predictions (used opencv to find whether the hand is moving or not) if motion of hand was found to be greater than a 
threshhold value used LSTM model else used the static model 


Static Folder :<br>
This folder has all the scripts , datasets used to make Static model <br>
"Static\DataSetCreation.py" : script used to create dataset<br>
"Static\datasetShuffle+Ann.ipynb" : script used to create model<br>
"Static\main.py" : This is the main script for static gesture predictions if you run this script live camera will open and start making predictions of ONLY static gestures <br>
Then we have various models and datasets , "Static\staticGestureANN.keras" is the first model which i trained it had many bugs which i fixed in subsequent models .<br>
The main dataset used is wrtWristDataset.xlsx which is combination of all other datasets.


Dynamic2 Folder :<br>
This folder has all scripts,datasets used to make dynamic model <br>
"Dynamic2\DataCreation.py" : this script is used to make the dataset <br>
"Dynamic2\DynamicModel.ipynb" this script is used to make model (LSTM)<br>
"DynamicDataset2.xlsx" is the dataset and the labels are contained in "Labels2.xlsx"<br>
"DynamicModel21.keras" is the final model used 
"main21.py" This is the main script for dynamic gesture prediction when you run this script camera will open up and start making predictions of ONLY dynamic gestures.
