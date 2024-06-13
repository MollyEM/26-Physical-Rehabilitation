import csv
import os
import sys
import numpy as np
import pandas as pd
from keras.models import load_model

def load_test_data(directory_path):
    # List all CSV files in the directory
    files = [file for file in os.listdir(directory_path) if file.endswith('.csv')]
    num_files = len(files)
    
    if num_files == 0:
        raise ValueError("No CSV files found in the specified directory.")

    # Initialize arrays to store data and labels
    data = np.zeros((num_files, 40, 50), dtype=np.float32)
    labels = np.zeros((num_files, 1), dtype=np.float32)

    # Read data from each CSV file
    for i, file in enumerate(files):
        file_path = os.path.join(directory_path, file)
        
        try:
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                # Read data and replace empty cells with zeros
                data[i] = np.nan_to_num(np.array([[float(entry) if entry.strip() else 0.0 for entry in row] for row in reader], dtype=np.float32))
        except ValueError as e:
            print(f"Error reading file '{file}': {e}")
            continue
    
    return data

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python classify.py path/to/csvs_folder")
        sys.exit(1)

    input_path = sys.argv[1]

    my_loaded_model = load_model('models/Classv7_78.keras', compile=False) 

    data = load_test_data(input_path)

    predictions = my_loaded_model.predict(data)
    predictions = int(np.argmax(predictions, axis=1))
    sys.exit(predictions)
