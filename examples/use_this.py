import posedetector

""" Hi to use every part of this program you need to uncomment each function"""

# 01 Add your video name here
file_name='mini_zaina480p'

# 02 Change the format (mp4) if needed
video_file_name=f'{file_name}.mp4'

# 03 run this to predict the keypoints
key_stop_process="a"
#posedetector.pose_detector_predict(video_file_name, key_stop_process)

# 04 run this to rename the name of the actors in the json
#posedetector.rename_actor(file_name)

# 05 run this to add value if some are missing in the json file
#posedetector.interpolate_missing_values(file_name)

# 06 run this to see graph visualization of the json values

figure = "esther"
point = "right_wrist"
frame_interval=10

#posedetector.json_to_graph(file_name, figure, point, frame_interval)