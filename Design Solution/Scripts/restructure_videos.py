#this script is useful to get the videos from the raw folder downloaded the unchanged folder
# onedrive Rehabilitation Assessment/UI-PRMD Dataset/Recorded Data and Videos/recorded by kinect
# into a single directory specified by output_directory with a nameing convention in the readme

# Dont run this script, it has output: "videos" directory

import os
import shutil
import sys

def copy_and_rename_avi_files(input_directory, output_directory):
    # Ensure the output folder exists
    os.makedirs(output_directory, exist_ok=True)

    # Walk through the input directory
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".avi"):
                original_file_path = os.path.join(root, file)

                # Extract information from the original file name
                filename, extension = os.path.splitext(file)
                prefix = "C_" if '1' in filename else "I_"
                leading_string = filename.split('1')[0] if '1' in filename else filename.split('2')[0]

                # Get the name of the parent directory
                parent_directory = os.path.basename(root)

                # Construct the new filename
                new_filename = f"{prefix}{leading_string}_{parent_directory}{extension}"

                # Construct the full output path
                output_path = os.path.join(output_directory, new_filename)

                # Copy the original file to the new directory with the new filename
                shutil.copy2(original_file_path, output_path)

                print(f"File copied and renamed: {output_path}")

def shorten_names(directory_path, mapping):
    """
    Rename files in the given directory based on the provided mapping dictionary.

    Parameters:
    - directory_path (str): Path to the directory containing files to be renamed.
    - mapping (dict): Dictionary with mapping rules for file renaming.
    """

    # Ensure the directory path is valid
    if not os.path.isdir(directory_path):
        print("Invalid directory path.")
        return

    # Iterate through each file in the directory
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)

        # Check if it's a file (not a directory)
        if os.path.isfile(file_path):
            # Apply mapping rules to the filename
            for old_str, new_str in mapping.items():
                filename = filename.replace(old_str, new_str)

            # Create the new file path with the updated filename
            new_file_path = os.path.join(directory_path, filename)

            # Rename the file
            os.rename(file_path, new_file_path)
            print(f'Renamed: {file_path} -> {new_file_path}')


if __name__ == "__main__":
    # Check if both input and output directories are provided as command-line arguments
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_directory> <output_directory>")
        sys.exit(1)

    input_directory = sys.argv[1]
    output_directory = sys.argv[2]

    copy_and_rename_avi_files(input_directory, output_directory)

    mapping = {"DeepSquat":"m01", "HurdleStep":"m02", "InlineLunge":"m03", "SideLunge":"m04", "Sidelunge":"m04","SitToStand":"m05", "SitToStnad":"m05", "StandingASLR":"m06", "StandingShoulderABD":"m07", "StandingShoulderEXT":"m08", "StandingShoulderIRER":"m09", "StandingShoulderScaption":"m10","subject0":"s"}
    shorten_names(output_directory, mapping)
    print("Done")
