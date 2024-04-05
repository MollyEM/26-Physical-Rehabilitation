#this script takes a video path as input, runs it through open pose, and has 2 outputs:
# 1. (in an argument specified directoy) mp4 videos with overlayed points
# 2. (in the (could be new) tableData directory) csv files with the estimated points
#    where each row is a frame, and 
#    where the columns are (joint_0_x, joint_0_y, joint_0_confidence, joint_1_x, joint_1_y, joint_1_confidence,...24)

import cv2
import os
import sys
import csv
import numpy as np


def insert_point(joint, frame, x, y, confidence, data_matrix):
    data_matrix[joint, frame, :] = (x, y, confidence)


def framestep(cap, data_matrix):
    
    # Get video properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    new_vid = []

    print("total frames to be analyzed: ", frame_count)
    curr_frame = 0
    i = 0
    while curr_frame < frame_count:
        ret, frame = cap.read()
        if curr_frame % 5 == 0:
            print("starting frame: ", i)
        new_vid.append(pose(frame, curr_frame, data_matrix))
        i+=1
        curr_frame+=1
    
    return new_vid
    
def squarify(frame):
    #make the video a square so that points can be overlaid correctly
    height, width, _ = frame.shape
    min_dim = min(height, width)

    # Calculate the cropping dimensions
    crop_height = (height - min_dim) // 2
    crop_width = (width - min_dim) // 2

    # Crop the image equally from both sides to make it a square
    return frame[crop_height:crop_height+min_dim, crop_width:crop_width+min_dim] , min_dim


def pose(frame, curr_frame, data_matrix):
    
    frame, size = squarify(frame)
    blob = cv2.dnn.blobFromImage(frame, 1/255, (size, size),
                             (0, 0, 0), swapRB=False, crop=True)

    # run forward pass to get the pose estimation
    net.setInput(blob)
    output = net.forward()
    
    # Extract joint locations
#    joint_locations = []

    for i in range(25): #hard-code the number of joints for convenience
    #for i in range(len(keypoints_mapping) - 1): # -1 because we dont want the last background point
        keypoint = output[0, i, :, :]
        min_val, confidence, min_loc, point = cv2.minMaxLoc(keypoint)
        
        insert_point(i, curr_frame, point[0], point[1], confidence, data_matrix)

#comments below are for viewing only the estimated points over the video
#        if confidence > 0.01:  # can adjust the confidence threshold if needed ???
#            joint_locations.append((i, 8 * int(point[0]), 8 * int(point[1]), confidence))
#        else:
#            joint_locations.append(None)

    #joint_locations contains the locations of the detected joints and corresponding index

#    for location in joint_locations:
#        if location:
#            index, x, y, confidence = location
#            cv2.circle(frame, (x, y), int(confidence*10), (0, 0, 255), -1)
#            #more confident points will be larger
#            #cv2.putText(image, str(index), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    return frame

####################################################################

def find_outliers(data_matrix, threshold=2):
    num_joints = data_matrix.shape[0]
    
    outlier_matrix = np.copy(data_matrix)
    good_matrix = np.copy(data_matrix)

    for joint_number in range(num_joints):
        # Extract x, y, confidence values for the specified joint
        x_values = data_matrix[joint_number, :, 0]
        y_values = data_matrix[joint_number, :, 1]

        # Calculate z-scores for x and y values
        x_zscores = (x_values - np.mean(x_values)) / np.std(x_values)
        y_zscores = (y_values - np.mean(y_values)) / np.std(y_values)

        # Identify outliers based on z-scores and threshold
        outliers = (np.abs(x_zscores) > threshold * (3/5)) | (np.abs(y_zscores) > threshold * 6/5)
        
        if joint_number in [8, 9, 12]:
            # Additional check for central position
            central_x = np.nanmedian(data_matrix[:, ~outliers, 0])
            central_y = np.nanmedian(data_matrix[:, ~outliers, 1])
            # Set as outliers if not central
            outliers |= ((np.abs(x_values - central_x) > threshold * 6) | 
                         (np.abs(y_values - central_y) > threshold * 36))

        # Set all outliers in the good data matrix to NaN for the current joint
        good_matrix[joint_number, outliers, :] = np.nan

        # Set all non-outliers in the outlier matrix to NaN for the current joint
        outlier_matrix[joint_number, ~outliers, :] = np.nan

    return good_matrix, outlier_matrix

#####################################################

# This needs improved logic
def fill_missing_points(points_array):
    num_joints, num_frames, num_dimensions = points_array.shape
    filled_points = np.copy(points_array)

    for joint_index in range(num_joints):
        for frame_index in range(num_frames):
            # Check if the current point is NaN
            if np.isnan(points_array[joint_index, frame_index]).any():
                # Find the nearest non-NaN frames before and after the current frame
                before_index = frame_index - 1
                while before_index >= 0 and np.isnan(points_array[joint_index, before_index]).all():
                    before_index -= 1

                after_index = frame_index + 1
                while after_index < num_frames and np.isnan(points_array[joint_index, after_index]).all():
                    after_index += 1

                # Use the average of the nearest non-NaN frames
                if before_index >= 0 and after_index < num_frames:
                    filled_points[joint_index, frame_index] = (
                        points_array[joint_index, before_index] + points_array[joint_index, after_index]
                    ) / 2
                elif before_index >= 0:
                    filled_points[joint_index, frame_index] = points_array[joint_index, before_index]
                elif after_index < num_frames:
                    filled_points[joint_index, frame_index] = points_array[joint_index, after_index]
                else:
                    # If no valid frames are found, leave the point as NaN
                    filled_points[joint_index, frame_index] = np.nan

    return filled_points

##########################################

def save_new_video(cap, path, output_directory, g_points, b_points, f_points):
   
    os.makedirs(output_directory, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(path))[0]
    new_file_name = f"{output_directory}/{base_name}_points.mp4"
    print("saving to", new_file_name)

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0) #reset the cap to the 0th frame
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    new_vid = []
    curr_frame = 0
    min_dim = 0
    
    while curr_frame < frame_count:
        ret, frame = cap.read()
        new_frame, min_dim = squarify(frame)
        
        for joint_index in range(f_points.shape[0]):
            point = f_points[joint_index, curr_frame]
            if not np.isnan(point).any():
                cv2.circle(new_frame, (8*int(point[0]), 8*int(point[1])), 5, (255, 255, 255), -1)       
        for joint_index in range(g_points.shape[0]):
            point = g_points[joint_index, curr_frame]
            if not np.isnan(point).any():
                cv2.circle(new_frame, (8*int(point[0]), 8*int(point[1])), 5, (100, 255, 255), -1)
        for joint_index in range(b_points.shape[0]):
            point = b_points[joint_index, curr_frame]
            if not np.isnan(point).any():
                cv2.circle(new_frame, (8*int(point[0]), 8*int(point[1])), 5, (0, 0, 255), -1)

        # Append the new frame to the new_vid list
        new_vid.append(new_frame)
        curr_frame+=1
    
    #prepare to write to mp4
    output_size = (min_dim, min_dim)
    print("size of frames:", min_dim)
    output_video = cv2.VideoWriter(new_file_name, cv2.VideoWriter_fourcc(*'mp4v'), 10, output_size)
    
    #write to mp4
    for frame in new_vid:
        output_video.write(frame)
    output_video.release()

    print("Video written!")
    print("Output directory content:", os.listdir(output_directory))

##################################################

def merge_filled_points(good_points, filled_points):
    num_joints, num_frames, _ = good_points.shape

    for joint_index in range(num_joints):
        for frame_index in range(num_frames):
            if np.isnan(good_points[joint_index, frame_index]).any():
                if np.isnan(filled_points[joint_index, frame_index]).any():
                    print("Both missing")
                else:
                    good_points[joint_index, frame_index] = filled_points[joint_index, frame_index]

##################################################

def save_to_csv(good_points, path):
    num_joints, num_frames, _ = good_points.shape

    os.makedirs("tableData", exist_ok=True)
    base_name = os.path.splitext(os.path.basename(path))[0]
    new_file_name = f"tableData/{base_name}.csv"
    print("saving to", new_file_name)

    with open(new_file_name, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        '''
        # Write header row with joint information - commented out because we dont need a header
        header = []
        for joint_index in range(num_joints):
            header.extend([f'joint_{joint_index}_x', f'joint_{joint_index}_y', f'joint_{joint_index}_confidence'])
        csvwriter.writerow(header)
        '''

        # Write data rows
        for frame_index in range(num_frames):
            row_data = []
            for joint_index in range(num_joints):
                x, y, confidence = good_points[joint_index, frame_index]
                row_data.extend([x, y, confidence])
            csvwriter.writerow(row_data)

##################################################

if __name__ == "__main__":
    # Check if both input and output directories are provided as command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python VideoToCsvViaOpenpose.py <input_video> <output_directory>")
        sys.exit(1)

    input_video = sys.argv[1]
    output_directory = sys.argv[2]
    input_video = os.path.abspath(sys.argv[1])
    output_directory = os.path.abspath(sys.argv[2])
    print(input_video)
    print(output_directory)

    # Define the keypoint mapping for this OpenPose body_25 model for visualization
    keypoints_mapping = {
    0:  "Nose", 1:  "Neck", 2:  "RShoulder", 3:  "RElbow", 4:  "RWrist", 5:  "LShoulder", 6:  "LElbow",
    7:  "LWrist", 8:  "MidHip", 9:  "RHip", 10: "RKnee", 11: "RAnkle", 12: "LHip", 13: "LKnee",
    14: "LAnkle", 15: "REye", 16: "LEye", 17: "REar", 18: "LEar", 19: "LBigToe", 20: "LSmallToe",
    21: "LHeel", 22: "RBigToe", 23: "RSmallToe", 24: "RHeel", 25: "Background"}
    
    #grab the video
    cap = cv2.VideoCapture(input_video)
    # Initialize the 3D matrix with zeros
    number_of_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    number_of_joints = 25
    data_matrix = np.zeros((number_of_joints, number_of_frames, 3))
    
    #load the model
    net = cv2.dnn.readNetFromCaffe('pose_deploy.prototxt', 'pose_iter_584000.caffemodel')
    
    my_video = framestep(cap, data_matrix)
    
    print("find outliers->")
    
    good_points, bad_points = find_outliers(data_matrix)
    print("fill missing points->")
    filled_points = fill_missing_points(good_points)
    print("save video->")
    save_new_video(cap, input_video, output_directory, good_points, bad_points, filled_points)
    cap.release()

    merge_filled_points(good_points, filled_points)
    save_to_csv(good_points, input_video)
    
    print("Done")