#this script will normalize every csv file in a directory, by column
import os
import pandas as pd
import sys

# Function to normalize each column
def normalize_column(column):
    mean = column.mean()
    std_dev = column.std()
    normalized_column = (column - mean) / std_dev
    return normalized_column

# Function to normalize entire DataFrame
def normalize_data(data):
    normalized_data = data.copy()
    for column in data.columns:
        normalized_data[column] = normalize_column(data[column])
    return normalized_data

# Function to normalize CSV files in a directory
def normalize_csv_files_in_directory(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.endswith('.csv'):
            input_file_path = os.path.join(input_directory, filename)
            output_file_path = os.path.join(output_directory, filename)
            normalize_csv_file(input_file_path, output_file_path)

def normalize_csv_file(input_file_path, output_file_path):
    # Read CSV file
    data = pd.read_csv(input_file_path, header=None)

    # Normalize data
    normalized_data = normalize_data(data)

    # Write normalized data to a new CSV file
    normalized_data.to_csv(output_file_path, index=False, header=False)

    print("Normalized data saved to", output_file_path)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py input_directory output_directory")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]
    normalize_csv_files_in_directory(input_directory, output_directory)

