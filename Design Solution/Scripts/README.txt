Scripts directory
---------------------

accuracyDS.py
	This python script takes a directory that contains csvs of shape 40x50,
	and runs them each through the best performing RNN model 'Squatv5' to generate
	accuracy scores for deep squat

all_steps.sh
	This bash script takes a directory of videos as input.
	Each video will be processed by openpose, smoothed, (segmented), normalized
	and then classified into which exercise, with classify.py
	If it is a deep squat, it will rate the accuracy with accuracyDS.py

AnimateCSV.ipynb
	This python file will animate a csv file with moving points on a graph
	Very useful for validation that data is good

augment.py
	This script will double the number of csvs in a directory, by randomly switching
	all points from the right arm to the left arm, right leg to the left leg, or both
	Be careful to only use this as is for symmetric exercises

classify.py
	This python script takes a directory that contains csvs of shape 40x50,
	and runs them each through the best performing RNN model 'Classv7_78' to generate
	predict which exercise was performed

episodeDivide.py
	This script divides a CSV into 10 csvs, based on where local maximums y joints are.
	It does not work perfectly, so its output needs to be checked (with AnimateCSV.ipynb).

half.py
	This python script reduces the fps of videos in a directory by a factor of 2
	This is useful for reducing openpose processing time of videos that were recorded
	in high quality/fps

interpolateAllColumns.py
	This python script interpolates all csvs in a directory to 40 rows (frames)
	piecewise linearly

normalize.py
	This python script normalizes (mean=0, sd=1) each column of a csv independently,
	for every csv file in a directory

openpose.py
	This script runs a specified video through openpose body_25, and geneartes a csv file.
	Be carefule with the threshold parameter for detecting and correcting outliers.
	Additionally, the predicted points are overlayed over the the video and saved in a new
	folder, so that the user can see the results

playAVI.py
	This python script will play an AVI video for the user.
	This is only useful for Mac users that are working with AVI video codec
	because Mac does not support AVI format

restructure_videos.py
	This script was only used once. It organized all of the video files downloaded from
	in the UI-PRMD thedatabase, and renamed them to a standardized naming convention

smoothCSV.py
	This python script does more outlier detection, correcting noisy points 
	to smooth them out
