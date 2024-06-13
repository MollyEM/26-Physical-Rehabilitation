#Play avi video

import cv2
import sys

def play_avi_video(video_file):
    # Open the video file
    cap = cv2.VideoCapture(video_file)

    # Check if the video file was successfully opened
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Get the video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create a window
    cv2.namedWindow("AVI Video Player", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("AVI Video Player", width, height)

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # Break the loop if the video has ended
        if not ret:
            break

        # Display the frame
        cv2.imshow("AVI Video Player", frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Release the video capture object and close the window
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Check if the input video file is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python play_video.py <input_video.avi>")
        sys.exit(1)

    # Get the input video file from the command-line argument
    input_file = sys.argv[1]

    # Play the AVI video
    play_avi_video(input_file)
