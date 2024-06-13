#!/usr/bin/env python
# coding: utf-8

#input: smoothed openpose joint positions for one episode
#40 frames as input

#change z points to zeros
#flip rows and columns
#center data

import pandas as pd
import numpy as np
import cv2
import csv
import sys
import os


def toSpatio(filename):
    frames = 40
    df = pd.read_csv(filename + ".csv", header=None)
    arr1 = df.to_numpy()

    print(arr1)

    #print(arr1)

    #insert zeros into every 3rd column
    j = range(2, 51, 2)
    k = 0 #[0] * frames
    raw_data = np.insert(arr1, j, k, axis = 1)
    raw_data_1 = raw_data.reshape(75 * frames)
    raw_data_2 = raw_data_1.reshape(75, frames, order = 'F')
    #arr1[:, range(2, len(arr1 + 1), 3)] = 0

    print(raw_data_2)

    #center data
    data_mean = np.mean(raw_data_2, axis = 0)
    centered_data = raw_data_2 - data_mean
    scaling_value = np.ceil(max(np.max(centered_data), abs(np.min(centered_data))))
    data_correct = centered_data / scaling_value

    #write to csv
    f = open(filename + "_smoothed.csv", 'w', newline = '')
    w = csv.writer(f)
    np.apply_along_axis(w.writerow, axis = 1, arr = data_correct)
    f.close()





if __name__ == "__main__":
    # Check if both input and output directories are provided as command-line arguments
    if len(sys.argv) != 3:
        print("Usage:  <input_CSV> ")
        exit(1)

    input_csv = sys.argv[1]
    input_video = os.path.abspath(sys.argv[1])
    print(input_video)
    
    toSpatio(input_csv)





