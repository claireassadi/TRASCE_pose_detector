import posedetector

""" Run this code to predict the pose detction """
# this will create a video and a json file

# Add your video name here
file_name='test'
# Change the format (mp4) if needed
video_file_name=f'{file_name}.mp4'

# Change the detection model if needed
yolo_model_path="models/yolov8m-pose.pt"

# the keyboard key pressed to stop the prediction process
# you can change it
key_stop_process="a"

# This  is the function that predict de keypoints
posedetector.pose_detector_predict(video_file_name, key_stop_process, yolo_model_path)