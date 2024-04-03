import posedetector

""" Run this code to see graph visualization of the json values """

# Specify the name of the video that you predicted
file_name='video_test'

# Specify the actor, the point and the frame interval that you want to see in the graph
figure = "keypoints_figure_2"
point = "nose"

# This funciton create the graph visualisation
posedetector.json_to_graph(file_name, figure, point)