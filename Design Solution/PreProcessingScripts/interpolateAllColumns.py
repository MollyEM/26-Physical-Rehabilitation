# this script takes a directory name as input, and outputs a new directory
# the new directory will have the same csv files as the input, but all with the same number of rows
# the column values are interpolated over a linear function

import pandas as pd
import os
import csv
import sys

def interpolate_values(original_list, m):
    n = len(original_list)

    # Calculate the step size for interpolation
    step_size = (n) / (m)

    # linear interpolation
    new_list = []
    for i in range(m):
        low = int(i * step_size)
        high = min(low + 1, n - 1)  # test high index doesn't exceed the bounds of the list
        slope = original_list[high] - original_list[low]
        fraction = (i * step_size) - low

        interpolated_value = original_list[low] + slope * fraction
        new_list.append(interpolated_value)

    return new_list

def interpolate_columns(df, m):
    # Interpolate each column separately
    interpolated_data = {}
    for column in df.columns:
        interpolated_data[column] = interpolate_values(df[column], m)
    return pd.DataFrame(interpolated_data)

def interpolate_values_for_all_csv(folder_path, output_folder, m):
    # get list of files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    
    # make output folder 
    os.makedirs(output_folder, exist_ok=True)

    # Loop through each CSV file
    for file in files:
        file_path = os.path.join(folder_path, file)
        output_file_path = os.path.join(output_folder, file)

        df = pd.read_csv(file_path)

        interpolated_df = interpolate_columns(df, m)

        #save interpolated DataFrame to a new CSV file
        interpolated_df.to_csv(output_file_path, index=False, header=False)



if __name__ == "__main__":
    # Check if a directory is provided as an argument
    if len(sys.argv) != 2:
        print("Usage: python script.py /path/to/directory")
    else:
        input_folder = sys.argv[1]
        output_folder = "same_size_csvs"
        
        new_frame_count = 40
        interpolate_values_for_all_csv(input_folder, output_folder, new_frame_count)
        print(f"Interpolated data saved in {output_folder} directory.")
