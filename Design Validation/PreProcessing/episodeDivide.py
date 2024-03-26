# This script will divide all csv files into the 10 episodes, from specified folder

import pandas as pd
import sys
import os


def find_local_extremes(numbers):
    local_maxes = []
    local_mins = []
    for i in range(3, len(numbers) - 3):
        if all(numbers[i] > numbers[j] for j in range(i - 2, i + 3) if j != i) and numbers[i] > max(numbers[i - 2], numbers[i + 2]):
            local_maxes.append(i)
        elif all(numbers[i] < numbers[j] for j in range(i - 2, i + 3) if j != i) and numbers[i] < min(numbers[i - 2], numbers[i + 2]):
            local_mins.append(i)

    return local_maxes, local_mins


def find_division_indexes(df):

    # extract average height of all points (less variable)
    average_column = df.iloc[:, 1::2].mean(axis=1)
    local_maxes, local_mins = find_local_extremes(average_column)

    while len(local_mins) > 11:
        #print(local_mins)
        min_difference = float('inf')
        min_indices = None
        for i in range(len(local_mins) - 1):
            difference = local_mins[i + 1] - local_mins[i]
            if difference < min_difference:
                min_difference = difference
                min_indices = (i, i + 1)

        if min_indices is not None:
            # Calculate the average of the two closest elements
            average_value = int((local_mins[min_indices[0]] + local_mins[min_indices[1]]) / 2)

            # Replace the two closest elements with their average
            local_mins[min_indices[0]] = average_value
            del local_mins[min_indices[1]]

    return sorted(local_mins)

def divide_csv(df, filename):
    # Define the row numbers to divide the CSV file
    row_numbers = find_division_indexes(df)
    #print(row_numbers)

    # Create a directory to store the divided CSV files
    output_directory = 'divided_csv_files'
    os.makedirs(output_directory, exist_ok=True)

    # Divide the DataFrame at specified row numbers and save each subset into a separate CSV file
    for i in range(len(row_numbers) - 1):
        start_idx = row_numbers[i]  
        end_idx = row_numbers[i + 1] - 1
        subset_df = df.iloc[start_idx:end_idx]
        output_filename = f"{filename.replace('.csv', '')}_e{i}.csv"
        output_path = os.path.join(output_directory, output_filename)
        subset_df.to_csv(output_path, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py directory_path")
        sys.exit(1)

    directory_path = sys.argv[1]

    if not os.path.isdir(directory_path):
        print(f"Error: Directory '{directory_path}' not found.")
        sys.exit(1)

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".csv"):
                input_csv_file = os.path.join(root, file)
                filename, extension = os.path.splitext(file)
                df = pd.read_csv(input_csv_file, header=None)
                divide_csv(df, filename)
                print(f"CSV file '{file}' successfully divided at specified row numbers.")




