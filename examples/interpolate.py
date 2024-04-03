import posedetector

""" Run this code to add valaue if they are missing in the JSON file """

# Specify the name of the video that you predicted
file_name='video_test'

# This function interpolate missing values with mean of x and y with the frame before and after
posedetector.interpolate_missing_values(file_name)