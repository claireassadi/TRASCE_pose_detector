import posedetector

""" Run this code to predict the pose detction """
# this will create a video and a json file

# Add your video name here
file_name='video_test'
# Change the format (mp4) if needed
video_file_name=f'{file_name}.mp4'

# Change the detection model if needed
yolo_model_path="models/yolov8m-pose.pt"

# the keyboard key pressed to stop the prediction process
key_stop_process="a"

# If False = simple working JSON / If True = you have a JSON augmented with more values (normilized/confidence/bounding-boxes)
augmented_json=False

# if True you see the render in real time / If False not (but the video is still exported)
# To end the process do: CTRL + C in the console 
show_video=True

# This  is the function that predict de keypoints
posedetector.pose_detector_predict(video_file_name, key_stop_process, yolo_model_path, augmented_json, show_video)