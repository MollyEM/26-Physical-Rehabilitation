#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility

import csv
import os,random

# The code is run on a CPU

from keras.models import Model
from keras.layers import Input, Conv1D, LSTM, Dense, Dropout, Activation, Flatten, concatenate, UpSampling1D
from keras.callbacks import EarlyStopping
from keras.optimizers import *
from keras.layers import Lambda

import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

from sklearn.metrics import mean_squared_error
from math import sqrt

import datetime
now = datetime.datetime.now


from keras.models import load_model 



def userTest(filename):

    model = load_model("my_models.OpenPose_SpatioTemporalNN_Vicon_Final.h5")
    
    n_dim = 75
    
    f = open(filename, 'r')
    c = csv.reader(f, delimiter = ',', quoting = csv.QUOTE_NONE)
    ctrain_x = np.zeros(shape = (1, timesteps, n_dim))
    
    i = 0
    for row in c:
        ctrain_x[0, :, i % 75] = row
        i += 1

    #print(ctrain_x)
    
    f.close()
    
    ctrain_x_2 = np.zeros((ctrain_x.shape[0], int(ctrain_x.shape[1]/2), ctrain_x.shape[2]))
    ctrain_x_4 = np.zeros((ctrain_x.shape[0], int(ctrain_x.shape[1]/4), ctrain_x.shape[2]))
    ctrain_x_8 = np.zeros((ctrain_x.shape[0], int(ctrain_x.shape[1]/8), ctrain_x.shape[2]))
    ctrain_x_2 = ctrain_x[:,::2,:]
    ctrain_x_4 = ctrain_x[:,::4,:]
    ctrain_x_8 = ctrain_x[:,::8,:] 
    
    #print(ctrain_x_8)

    # Reorder the data dimensions to correspond to the five body parts
    ctrainx =  reorder_data(ctrain_x)
    ctrainx_2 =  reorder_data(ctrain_x_2)
    ctrainx_4 =  reorder_data(ctrain_x_4)
    ctrainx_8 =  reorder_data(ctrain_x_8)
    
    
    #Split Sequences???
    


    #prediction
    pred = model.predict([ctrainx, ctrain_x_2, ctrain_x_4, ctrain_x_8])
    print("Your accuracy rating for " + filename + " is: ", pred)
    plt.plot(pred,'s', color='red', label='Prediction', linestyle='None', alpha = 0.5, markersize=6)
    
    
    
if __name__ == "__main__":
    # Check if both input and output directories are provided as command-line arguments
    if len(sys.argv) != 2:
        print("Usage:  <input_CSV> ")
        exit(1)

    input_csv = sys.argv[1]
    input_video = os.path.abspath(sys.argv[1])
    print(input_video)
    
    userTest(input_csv)

