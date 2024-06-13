#This function smooths over the outliers for all outliers in any column for all csvs in the specified directory

import pandas as pd
import numpy as np
import sys
import os

def replace_outliers(data, window_size=5, threshold=2.0):
    """
    Replace outliers in each column with the average of adjacent points within a specified window.

    Parameters:
    - data: pandas DataFrame
    - window_size: int, the size of the window for calculating the average (default is 5)
    - threshold: float, the threshold for identifying outliers (default is 2.0)

    Returns:
    - data: pandas DataFrame, with outliers replaced
    """
    for column_name in data.columns:
        x = data[column_name].values

        # Identify outliers based on the average of points within the window
        for i in range(window_size, len(x) - window_size):
            window_avg = x[i - window_size:i + window_size + 1].mean()
            if np.abs(x[i] - window_avg) > threshold * x.std():
                x[i] = window_avg

        # update the dataframe
        data[column_name] = x
    return data

def moving_average(data):
    smoothed_data = pd.DataFrame()

    for i in range(0, len(data.columns)):
        x_col = data.columns[i]

        x = data[x_col].values

        # Apply the new weights for the moving average
        x_smoothed = 0.1 * pd.Series(x).shift(-1, fill_value=x[-1]).values + 0.8 * x + 0.1 * pd.Series(x).shift(1, fill_value=x[0]).values
        smoothed_data[x_col] = x_smoothed

    return smoothed_data

def smooth_and_save(input_file):
    # Load your CSV data into a pandas DataFrame
    df = pd.read_csv(input_file, header=None)

    replace_outliers(df)
    # adjust each point with a moving average of the previous 2 points
    smoothed_data = moving_average(df)

    # Save the smoothed data to a new CSV file

    output_file = os.path.join('smoothedOutliers', os.path.basename(input_file))
    smoothed_data.to_csv(output_file, index=False, header=False)
    print(f'Smoothed data saved to {output_file}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py path/to/input_directory")
        sys.exit(1)

    directory_path = sys.argv[1]

    os.makedirs('smoothedOutliers', exist_ok=True)

    for root, _, files in os.walk(directory_path):
        # Process each file in the directory
        for file in files:
            # Create the full file path
            file_path = os.path.join(root, file)
            # Apply smooth_and_save function to the file
            smooth_and_save(file_path)

