#!/bin/bash

#take in a filename + path from the user as $1, $2 output directory of video of overlayed points

python openpose.py $1 "/outVideos"

python smoothCSV.py "/tableData"

python interpolateAllColumns.py "./smoothedOutliers"

python SingleEpisodePreprocess.py "./same_size_csvs/${$1%.*}.csv"

python ReshapeInput.py "./same_size_csvs/${$1%.*}_smoothed.csv"

pause