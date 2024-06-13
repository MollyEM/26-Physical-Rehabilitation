#!/bin/bash

# this script will process all of the single episode videos
# in specified directory, and run them through the myModel.py script
# individually. All the intermediate steps are deleted afterwords
# for housekeeping and so this can immediately be used again
if [ $# -eq 0 ]; then
    echo "Usage: $0 <directory_with_videos>"
    exit 1
fi

directory=$1
echo "Processing videos in folder: $directory"

mkdir vids_w_points
for file in "$directory"/*; do
    if [ -f "$file" ]; then
        echo "$file"
        python openpose.py "$file" vids_w_points
    fi
done

#python episodeDivide.py ___ removed because it is better to manually divide
python smoothCSV.py tableData
python interpolateAllColumns.py smoothedOutliers

mkdir norm
python normalize.py same_size_csvs norm

python classify.py "norm"
result=$?
echo "Classification result for $file"
case $result in
    0)
        echo "deep squat"
        echo "Accuracy:"
        python accuracyDS.py "norm"
        acc=$?;;
    1)
        echo "inline lunge";;
    2)
        echo "Side Lunge";;
    *)
        echo "Unknown classification result: $result";;
esac

rm -rf norm
rm -rf tableData
rm -rf smoothedOutliers
rm -rf same_size_csvs

echo "---Done---"
