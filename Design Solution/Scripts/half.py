import os
import cv2

def remove_every_other_frame(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith('.MOV'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            # Open the video file
            cap = cv2.VideoCapture(input_path)
            if not cap.isOpened():
                print(f"Error: Could not open video file '{input_path}'")
                continue

            # Get video properties
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Create video writer for output
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Specify codec
            out = cv2.VideoWriter(output_path, fourcc, fps / 2, (width, height))

            # Process frames
            frame_count = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                # Write every other frame
                if frame_count % 2 == 0:
                    out.write(frame)

                frame_count += 1

            # Release resources
            cap.release()
            out.release()

            print(f"Frames removed from '{input_path}' and saved to '{output_path}'")

# Specify input and output directories
input_directory = 'NandC'
output_directory = 'NandChalf'

# Call the function to remove every other frame
remove_every_other_frame(input_directory, output_directory)

