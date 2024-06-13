import os
from pathlib import Path
import pandas as pd
import random

def swap_columns(file_path):
    """
    Swaps specified columns pairs in a CSV file using pandas.

    Args:
        file_path (str): The path to the CSV file.
        column_pairs (list of tuples): List of column index pairs to swap.

    Returns:
        None
    """
    pairs_arm = [(4, 10), (5, 11), (6, 12), (7, 13), (8, 14), (9, 15)]
    pairs_leg = [
        (18, 24), (19, 25), (20, 26), (21, 27), (22, 28), (23, 29),
        (44, 38), (45, 39), (46, 40), (47, 41), (48, 42), (49, 43)
    ]
    column_pairs = random.choice([pairs_arm, pairs_leg, pairs_arm + pairs_leg])
    try:
        df = pd.read_csv(file_path, header=None)
        for pair in column_pairs:
            column1_index, column2_index = pair
            columns = df.columns.tolist()
            columns[column1_index], columns[column2_index] = columns[column2_index], columns[column1_index]
            df = df[columns]
        new_file_path = file_path.replace('.csv', '_swap.csv')
        df.to_csv(new_file_path, index=False, header=False)
        print(f"Swapped CSV saved as '{new_file_path}'.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def swap_columns_in_directory(directory):
    """
    Swaps specified columns pairs in every CSV file in the specified directory.

    Args:
        directory (str): The path to the directory containing CSV files.
        column_pairs (list of tuples): List of column index pairs to swap.

    Returns:
        None
    """
    try:
        directory_path = Path(directory)
        for file_path in directory_path.glob("*.csv"):
            if "swap" not in file_path.name:
                swap_columns(str(file_path))
    except FileNotFoundError:
        print(f"Directory '{directory}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    column_pairs = [(4, 10), (5, 11), (6, 12), (7, 13), (8, 14), (9, 15)]
    swap_columns_in_directory(directory)

