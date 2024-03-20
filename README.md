# Pose Detector from Trasce Project

## Overview
- Here is a code for predicting the rythme in theatrical staging
- TRASCE is a research in charge of finding trasces in thatrical field

## Technical information
- running on python 3.10 because of lap module
- I had to download separatly

## HOW TO USE THIS PROGRAM
- clone this repo
- charge your videos in the **input-files** folder
- in the **examples** folder 
- add the name of the file you want to predict _yourfile.extension_
- run **use_this.py**
- the prediction is in **export-results** folder
- you get a _video_ and a _json_

### the json file
- you get _frame by frame_ the pixel coordinates (x,y) for each 17 COCO keypoints and this for every person
- keypoint_figure_1 = id 1 in the video export