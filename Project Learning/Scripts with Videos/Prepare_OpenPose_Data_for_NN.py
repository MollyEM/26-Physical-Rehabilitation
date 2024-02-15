#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[1]:


#Directions

#make sure you have installed cv2 with command: 
#  pip install opencv-python
#download the file called pose_iter_584000.caffemodel which is saved in this dropbox:
#  https://www.dropbox.com/s/3x0xambj2rkyrap/pose_iter_584000.caffemodel?dl=0
#download the file called pose_deploy.prototxt which is saved here:
#  https://github.com/CMU-Perceptual-Computing-Lab/openpose/tree/master/models/pose/body_25

#save both of these files in the same folder as this ipynb
#save a video in the same folder or subfolder


#issues:

# the model keeps recognizing exercise equipment in the background as body parts,
# i think using a different model(for multiple people simultaneously), 
# or adjusting confidence could help with this

# i could only make the scaling work by cropping the images to squares first
# not a big deal now with our training data, but it could cause problems in the future

# i think most of these .avi videos are 30 fps. if not, framestep() will need to be updated

# this script does not save the video, it only displays it in a popup window. 


# In[ ]:





# In[ ]:





# In[5]:


import cv2

import csv

def video_to_CSV(filename, frames = 240):
    # Open the video file
    cap = cv2.VideoCapture(filename)

    if not cap.isOpened():
        print("Cannot open camera")
        return

    # Define the keypoint mapping for this OpenPose body_25 model
    keypoints_mapping = {
        0:  "Nose", 1:  "Neck", 2:  "RShoulder", 3:  "RElbow", 4:  "RWrist", 5:  "LShoulder", 6:  "LElbow",
        7:  "LWrist", 8:  "MidHip", 9:  "RHip", 10: "RKnee", 11: "RAnkle", 12: "LHip", 13: "LKnee",
        14: "LAnkle", 15: "REye", 16: "LEye", 17: "REar", 18: "LEar", 19: "LBigToe", 20: "LSmallToe",
        21: "LHeel", 22: "RBigToe", 23: "RSmallToe", 24: "RHeel"
    }
    #load the model
    net = cv2.dnn.readNetFromCaffe('pose_deploy.prototxt', 'pose_iter_584000.caffemodel')

    #Write frame information of joint locations into a csv file
    f = open(filename + ".csv", 'w', newline='')
    w = csv.writer(f)
    #for keypoint, label in keypoints_mapping:
        #w.write(str(keypoints_mapping.items())
    #w.writerow(keypoints_mapping.values())
    
    def framestep(cap):
        # Get video properties
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        print()
        print("fps: %d" % (fps))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        new_vid = []
        stepsize = frame_count // frames # reset to fps/10
        print(stepsize)
        print("total frames to be analyzed: ", frame_count / stepsize)
        curr_frame = 0
        i = 0
        # Loop until the whole video has been read, or the requested number of frames are reached
        while curr_frame < frame_count and i < frames:
            ret, frame = cap.read()
            if curr_frame % stepsize == 0:
                print("starting frame: ", i)
                new_vid.append(pose(frame))
                i+=1
            curr_frame+=1

        return new_vid
        
    def squarify(frame):
        height, width, _ = frame.shape
        min_dim = min(height, width)

        # Calculate the cropping dimensions
        crop_height = (height - min_dim) // 2
        crop_width = (width - min_dim) // 2

        # Crop the image equally from both sides to make it a square
        return frame[crop_height:crop_height+min_dim, crop_width:crop_width+min_dim] , min_dim

    def pose(frame):
        frame, size = squarify(frame)
        blob = cv2.dnn.blobFromImage(frame, 1/255, (size, size),
                                (0, 0, 0), swapRB=False, crop=True)

        # run forward pass to get the pose estimation
        net.setInput(blob)
        output = net.forward()
        
        # Extract joint locations
        joint_locations = []
        csv_joint_locations = []

        for i in range(len(keypoints_mapping)): #-1 bc we dont want point for the background
            keypoint = output[0, i, :, :]
            min_val, confidence, min_loc, point = cv2.minMaxLoc(keypoint)

            #if confidence > 0.1:  # can adjust the confidence threshold if needed ???
            joint_locations.append((8 * int(point[0]), 8 * int(point[1]), 0)) #for testing/human readable
            csv_joint_locations.append(8 * int(point[0])) #to be printed into csv
            csv_joint_locations.append(8 * int(point[1])) #to be printed into csv
            csv_joint_locations.append(0) #to be printed into csv
            '''else:
                joint_locations.append(None) #for testing/human readable
                csv_joint_locations.append(8 * int(point[0])) #to be printed into csv
                csv_joint_locations.append(8 * int(point[1])) #to be printed into csv
            '''
        #joint_locations contains the locations of the detected joints and corresponding index

        '''for location in joint_locations:
            if location:
                x, y, index = location
                cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
                #cv2.putText(image, str(index), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        '''        
        #print joint locations into a csv file
        w.writerow(csv_joint_locations)
        
        return frame


    #write the information + circles onto each frame and pop up a window for each frame
    my_video = framestep(cap)
    size = my_video[0].shape[1], my_video[0].shape[0]
    print(size)
    '''out = cv2.VideoWriter("real.avi", cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

    for i in range(len(my_video)):
        out.write(my_video[i])
        cv2.imshow("video", my_video[i])
        cv2.waitKey(0)

    cv2.destroyAllWindows()
    out.release()
    '''
    cap.release()
    f.close()

    exit(1)


# In[1]:


#to write the frames into a video format for viewer presentation
'''
cap = cv2.VideoCapture(video_path)

def test():
    size = (1080, 1080)
    out = cv2.VideoWriter("deep.avi", cv2.VideoWriter_fourcc(*'DIVX'), 30, size)
    for i in range(0, 200):
        f, s = squarify(cap.read()[1])
        s
        out.write(f)
    
    out.release()

test()
cap.release()
'''


# In[7]:


#split the movements in the file into 10 reps (240 frames/arrays)
#estimating by dividing by 10 for now to seperate the reps
#future me note: can divide each rep by the local minimum of the hip value within x number of frames to obtain the full repinfo

import numpy as np

'''
Reads the joint location data from the provided csv file, assuming that the columns are joint positions, and
the rows are individual frames. A numpy array is returned with the columns representing frames per episode,
and the rows representing joint positions * episodes * subjects.
'''
def episode_split(filename, frames):
    #load file into a single array (all 240 arrays into 1)
    with open(filename, 'r', newline='') as f:
        w = csv.reader(f, delimiter = ',', quoting = csv.QUOTE_NONE)

        raw_data = np.zeros(shape = (frames, 75))

        # Populate raw_data with each row representing 1 frame
        i = 0
        for row in w:
            if i >= frames:
                break

            raw_data[i, :] = row
            #print("i: ", i, " row: ", row)
            i += 1

        #print(raw_data.shape)

        raw_data_1 = np.reshape(raw_data, 75 * frames)
        #print(raw_data_1)
        raw_data_2 = raw_data_1.reshape(75, frames, order = 'F')
        #print(raw_data_2)

        # Split data into 10 episodes, with an equal number of frames per episode and the last episode getting the remainder

        # Number of frames to keep in each episode, rounded down
        n = int(frames / 10) # nframes/10

        split_data = np.zeros(shape = (75 * 10, n)) # list of 10 lists, first 9 with n frames of joint locations, 10th with all the rest
        for i in range(0, 9):
            split_data[i * 75:(i + 1) * 75, :] = raw_data_2[:, i * n:(i + 1) * n]

        split_data[9 * 75:, :] = raw_data_2[:, 9 * n:]
        #split_data.append(raw_data_2[9 * n:len(xs)]) # put the rest of the frames into episode 10

        #print(len(split_data))
        print(split_data)
        f.close()
        return np.array(split_data)

#print(episode_split("Videos/subject001/DeepSquat1.avi.csv", 10))


# In[10]:


frames_to_analyze = 250
episodes = 10
features = 75

subjects = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11] # there is no subject 2

#this step is applied after every subject has been analyzed by openpose and split by episode
#correct data
for i in subjects:
    video_to_CSV("Videos/subject0" + ("0" if i < 10 else '') + str(i) + "/DeepSquat1.avi", frames_to_analyze)
    
#incorrect data
#for i in subjects:
    #video_to_CSV("Videos/subject0" + ("0" if i < 10 else '') + str(i) + "/DeepSquat2.avi", frames_to_analyze)

#correct data
combined = np.zeros(shape = (len(subjects) * episodes * features, frames_to_analyze//10))
ind = 0
for i in subjects:
    combined[ind * episodes * features:(ind + 1) * episodes * features, :] = episode_split("Videos/subject0" + ("0" if i < 10 else '') + str(i)  + "/DeepSquat1.avi.csv", frames_to_analyze)
    ind += 1
    
#incorrect data
'''
combined_inc = np.zeros(shape = (len(subjects) * episodes * features, frames_to_analyze//10))
ind = 0
for i in subjects:
    combined_inc[ind * episodes * features:(ind + 1) * episodes * features, :] = episode_split("Videos/subject0" + ("0" if i < 10 else '') + str(i)  + "/DeepSquat2.avi.csv", frames_to_analyze)
    ind += 1  
'''
combined[combined == ''] = 0
combined = combined.astype(float)
#print(combined.shape)
print(combined)

#combined_inc[combined_inc == ''] = 0
#combined_inc = combined_inc.astype(float)

#get the mean of every first value
data_mean = np.mean(combined, axis = 0)
#Data_mean = repmat(mean(Correct_Xm,2), 1, size(Correct_Xm,2));

#inc_data
#data_mean_inc = np.mean(combined_inc, axis = 0)

centered_data = combined - data_mean

#inc_data
#centered_data_inc = combined_inc - data_mean_inc

# Scale the data between -1 and 1
scaling_value = np.ceil(max(np.max(centered_data), abs(np.min(centered_data))))
data_correct = centered_data / scaling_value


# Scale the incorrect data between -1 and 1
#scaling_value_inc = np.ceil(max(np.max(centered_data_inc), abs(np.min(centered_data_inc))))
#data_incorrect = centered_data_inc / scaling_value_inc


#print(len(data_correct))
print(data_correct)


# In[43]:


# Indices of episodes to keep
good_indices = [(2, 10), (12, 20), (22, 30), (32, 40), (42, 60), (62, 63), (65, 70), (72, 80), (82, 84), (86, 100)]

# Remove the first episodes for most of the subjects due to missing values during the data recording and also remove a few other inconsistent episodes
data_correct_red = np.zeros(shape = (90 * features, len(data_correct[0])));
i = 0 # number of episodes copied so far
for ind in good_indices:
    eps = ind[1] - ind[0] + 1 # number of episodes to copy for this range
    
    # Copy all of the features for every episode within this index's range
    data_correct_red[i * features:(i + eps) * features, :] = data_correct[(ind[0] - 1) * features:ind[1] * features, :]
    
    i += eps # record the number of episodes copied so far
    #print("episodes this time: ", eps, " total episodes so far: ", i)
    
#print(data_correct_red[6600:6750, :])


# Remove the first episodes for most of the subjects due to missing values during the data recording and also remove a few other inconsistent episodes
data_incorrect_red = np.zeros(shape = (90 * features, len(data_incorrect[0])));
i = 0 # number of episodes copied so far
for ind in good_indices:
    eps = ind[1] - ind[0] + 1 # number of episodes to copy for this range
    
    # Copy all of the features for every episode within this index's range
    data_incorrect_red[i * features:(i + eps) * features, :] = data_incorrect[(ind[0] - 1) * features:ind[1] * features, :]
    
    i += eps # record the number of episodes copied so far
    #print("episodes this time: ", eps, " total episodes so far: ", i)


# In[12]:


f = open('data_correct.csv', 'w', newline = '')
w = csv.writer(f)
np.apply_along_axis(w.writerow, axis = 1, arr = data_correct)

f.close()


'''
f = open('data_incorrect.csv', 'w', newline = '')
w = csv.writer(f)
np.apply_along_axis(w.writerow, axis = 1, arr = data_incorrect)

f.close()
'''

