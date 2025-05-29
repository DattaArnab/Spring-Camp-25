import numpy as np

def isstatic(landmark_history, threshold=0.05):
    if len(landmark_history) < 2:
        return True
    
    distance = np.mean(np.linalg.norm(np.array(landmark_history[-1]) - np.array(landmark_history[-2])))
    return distance < threshold