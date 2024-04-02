from ultralytics import YOLO
import json
import cv2
import os

def pose_detector_predict(video_file_name, key_stop_process):
    """ 
    Predict the Pose Detection
    and export the Video and the Json 
    """

    # Ultralytics Pose Model
    model = YOLO("src/posedetector/yolov8m-pose.pt")

    # Folder path and filename
    video_path = f'input-files/{video_file_name}'
    cut_file_name = os.path.splitext(os.path.basename(video_path))[0]

    # Cap = capture -> give the video path to cv2
    cap = cv2.VideoCapture(video_path)
    ret = True

    # get video infos
    fps = int(cap.get(cv2.CAP_PROP_FPS))                    # number of frame per seconds ex: 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))          # width
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))        # height
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))    # get the total number of frames of the video ex: 350


    # initialize the start of the frame count and the data list for the json file
    frame_number = 1
    data=[]

    # Set the 17 COCO keypoints name to assagin for each keypoint
    keypoints_names = [
                    'nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear',
                    'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow',
                    'left_wrist', 'right_wrist', 'left_hip', 'right_hip',
                    'left_knee', 'right_knee', 'left_ankle', 'right_ankle'
                    ]
    
    # Video export path
    output_video_path = f'export-results/videos/{cut_file_name}.avi'
    video_export = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'MJPG'), 10, (width, height))


    # Start of the CV2 video runing
    while ret:
        ret, frame = cap.read()

        if ret:
        
            # GET THE REULTS FROM YOLOV8 POSE MODEL
            results = model.track(frame, persist=True)
            frame = results[0].plot()

            # get the frame number each loop
            frame_data = {"frame": frame_number}
            
            # get the Boxes and Keypoints results from yolov8
            for result in results:
                boxes = result.boxes  # Boxes object for bbox outputs
                keypoints = result.keypoints.xy  # Keypoints object for keypoint outputs
                
                for i, box in enumerate(boxes):
                    
                    box_id = box.id
                    box_id = int(box_id)
                    keypoints_figure_number = f"keypoints_figure_{box_id}"
                    
                    keypoints_names = [
                    'nose', 'left_eye', 'right_eye', 'left_ear', 'right_ear',
                    'left_shoulder', 'right_shoulder', 'left_elbow', 'right_elbow',
                    'left_wrist', 'right_wrist', 'left_hip', 'right_hip',
                    'left_knee', 'right_knee', 'left_ankle', 'right_ankle'
                    ]
                    
                    # Convert tensors array tp python list
                    keypoints_list = keypoints[i].tolist()

                    # Create dictionnary for each keypoints with x and y values
                    keypoints_dicts = [{"x": k[0], "y": k[1]} for k in keypoints_list]

                    
                    # Add x and y values with the associated name
                    keypoints_with_names = {name: coord for name, coord in zip(keypoints_names, keypoints_dicts)}

                    # Add keypoints to frame_data
                    frame_data[keypoints_figure_number] = keypoints_with_names


            # Add the data of the frame to the list
            data.append(frame_data)
            

            # Add text on the frame
            font = cv2.FONT_HERSHEY_SIMPLEX 
            frame_count_str = str(frame_count)
            cv2.putText(frame, str(frame_number), (50, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)
            cv2.putText(frame, f'/{frame_count_str} frames', (110, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)
            cv2.putText(frame, f'{fps}/sec', (400, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)

            print(f'frame : {frame_number}/{frame_count_str} total frame, is processed...')

            frame_number += 1
            
            # Write the export video
            video_export.write(frame)
            
            # Show CV2
            cv2.imshow('frame', frame)
            if cv2.waitKey(25) & 0xFF == ord(key_stop_process):
                break


    """ End of the video export """
    cap.release() 
    # Closes all the frames 
    cv2.destroyAllWindows() 
    video_export.release() 
    print("The video was successfully saved") 

    """ export of json """
    # Create the output file path
    output_file_path = os.path.join(os.path.dirname('export-results/json/'), f'{cut_file_name}.json')

    # Write the data in a json file
    with open(output_file_path, 'w') as f:
        json.dump(data, f, indent=4)