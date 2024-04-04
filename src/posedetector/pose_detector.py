from ultralytics import YOLO
import json
import cv2
import os
import urllib.request
import shutil

def pose_detector_predict(video_file_name, key_stop_process, yolo_model_path, augmented_json, show_video):
    """ 
    Predict the Pose Detection
    and export the Video and the Json 
    """
    # Function to download the file from a given URL to a specified destination
    def download_file(url, destination):
        try:
            with urllib.request.urlopen(url) as response, open(destination, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
            print("YOLOv8 pose model downloaded.")
        except Exception as e:
            print(f"Something went wrong downloading the YOLOv8 model: {e}")

    # URL of the YOLOv8 model
    url_du_fichier = "https://github.com/ultralytics/assets/releases/download/v8.1.0/yolov8m-pose.pt"
    
    # Destination path to save the model
    chemin_destination = "models/"

    # Check if the YOLOv8 model file exists in the models directory
    if not os.path.exists(chemin_destination):
        # If not, download the model
        download_file(url_du_fichier, chemin_destination)
    else:
        print("YOLOv8 pose model already exists.")

    # Ultralytics Pose Model
    model = YOLO(yolo_model_path)

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
    data_augmented=[]

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
            
            if augmented_json is False:
                # get the Boxes and Keypoints results from yolov8
                for result in results:
                    boxes = result.boxes  # Boxes object for bbox outputs
                    keypoints = result.keypoints.xy  # Keypoints object for keypoint outputs

                    for i, box in enumerate(boxes):
                        box_id = int(box.id)
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
            else:
                 # get the Boxes and Keypoints results from yolov8
                for result in results:
                    boxes = result.boxes  # Boxes object for boxes outputs
                    keypoints_xy = result.keypoints.xy  # xy value of each Keypoints
                    keypoints_xyn = result.keypoints.xyn  # xyn value of each Keypoints
                    keypoints_conf = result.keypoints.conf  # confidence value of the prédiction (17 values for each keypoint)

                    # get each boxes id
                    for i, boxe in enumerate(boxes):
                        boxe_id = int(boxe.id)  # get boxe id
                        keypoints_figure_number = f'keypoints_figure_{boxe_id}'  # assign boxe_id to keypoint_figure

                        # Convert keypoints tensors to python list
                        keypoints_xy_list = keypoints_xy[i].tolist()
                        keypoints_xyn_list = keypoints_xyn[i].tolist()
                        keypoints_conf_list = keypoints_conf[i].tolist()

                        # Convert boxes tensors to python list
                        boxe_xyxy_list = boxe.xyxy.tolist()

                        # List of dicts for keypoints with xy / xyn / conf values
                        keypoints_dicts_xy = [{"x": k[0], "y": k[1]} for k in keypoints_xy_list]
                        keypoints_dicts_xyn = [{"xNormalized": k[0], "yNormalized": k[1]} for k in keypoints_xyn_list]
                        keypoints_dicts_conf = [{"confidence": k} for k in keypoints_conf_list]

                        # Extract the single bounding box from the list
                        bounding_box = boxe_xyxy_list[0]

                        # Associer chaque valeur de keypoints avec son nom correspondant
                        keypoints_with_names = {}
                        # BOUNDING BOX
                        for kp_name, coord_kp_xy, coord_kp_xyn, coord_kp_conf \
                                in zip(keypoints_names, keypoints_dicts_xy, keypoints_dicts_xyn, keypoints_dicts_conf):
                            coord_kp_xy.update(coord_kp_xyn)  # Fusionner les deux dictionnaires
                            coord_kp_xy.update(coord_kp_conf)  # Fusionner les deux dictionnaires
                            keypoints_with_names[kp_name] = coord_kp_xy

                        # Ajouter la bounding box à la liste de keypoints
                        keypoints_with_names["bounding_box"] = {
                            "x": bounding_box[0],
                            "y": bounding_box[1],
                            "x2": bounding_box[2],
                            "y2": bounding_box[3]
                        }

                        # Ici on inscrit les valeurs dans le JSON
                        frame_data[keypoints_figure_number] = keypoints_with_names
                
                data_augmented.append(frame_data)


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
            
            # Write the json video
            if augmented_json is False:
                """ export of json """
                # Create the output file path
                output_file_path = os.path.join(os.path.dirname('export-results/json/'), f'{cut_file_name}.json')

                # Write the data in a json file
                with open(output_file_path, 'w') as f:
                    json.dump(data, f, indent=4)
            else:
                output_file_path_augmented = os.path.join(os.path.dirname('export-results/json/'), f'{cut_file_name}.json')

                with open(output_file_path_augmented, 'w') as f:
                    json.dump(data_augmented, f, indent=4)

            # Show CV2
            if show_video is True:
                cv2.imshow('frame', frame)
                if cv2.waitKey(25) & 0xFF == ord(key_stop_process):
                    break


    """ End of the video export """
    cap.release() 
    # Closes all the frames 
    cv2.destroyAllWindows() 
    video_export.release() 
    print("The video and the json file were successfully saved")