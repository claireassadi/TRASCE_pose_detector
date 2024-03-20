from ultralytics import YOLO
import json
import cv2
import os


def pose_detector_predict(file_name):
    """ This"""

    # pose model from ultralytics
    model = YOLO("yolov8m-pose.pt")

    video_path = f'input-files/{file_name}'
    cut_file_name = os.path.splitext(os.path.basename(video_path))[0]

    cap = cv2.VideoCapture(video_path)
    ret = True

    fps = int(cap.get(cv2.CAP_PROP_FPS))                    # nombre de frame par secondes de la vidéo ex: 30
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))          # width
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))        # height
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))    # compte le nombre de frame présente dans la vidéo ex: 350

    frame_number = 1
    data=[]

    output_video_path = f'export-results/videos/{cut_file_name}.avi'
    video_export = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'MJPG'), 10, (width, height))

    
    while ret:
        ret, frame = cap.read()

        if ret:
        
            # AFFICHER LES RESULTATS DES PREDICTIONS DE YOLOV8
            results = model.track(frame, persist=True)
            frame = results[0].plot()

            # Récupérer les résultats des prédictions
            frame_data = {"frame": frame_number}
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
                    
                    # Convertir les tenseurs en listes Python standard
                    keypoints_list = keypoints[i].tolist()

                    # Créer une liste de dictionnaires pour les keypoints avec des clés "x" et "y"
                    keypoints_dicts = [{"x": k[0], "y": k[1]} for k in keypoints_list]

                    
                    # Associer chaque valeur de keypoints avec son nom correspondant
                    keypoints_with_names = {name: coord for name, coord in zip(keypoints_names, keypoints_dicts)}

                    # Ajouter les keypoints à la frame_data
                    frame_data[keypoints_figure_number] = keypoints_with_names
                    """ POSITION EN PIXEL EN FONCTION DE L'IMAGE"""
                    """
                    # Associer chaque valeur de keypoints avec son nom correspondant et calculer les positions de pixels
                    keypoints_with_names_and_pixels = {}
                    for name, coord in zip(keypoints_names, keypoints_dicts):
                        x_pixel = coord["x"] * width  # Position du pixel x
                        y_pixel = coord["y"] * height  # Position du pixel y
                        keypoints_with_names_and_pixels[name] = {
                            "x": coord["x"],
                            "y": coord["y"],
                            "point_xy": (x_pixel, y_pixel)  # Ajouter les positions de pixels
                        }
                    
                    # Ajouter les keypoints à la frame_data
                    frame_data[keypoints_figure_number] = keypoints_with_names_and_pixels
                    """

            # Ajouter les données de la frame à la liste de données
            data.append(frame_data)
            frame_number += 1

            frame_count_str = str(frame_count)

            font = cv2.FONT_HERSHEY_SIMPLEX 
            cv2.putText(frame, str(frame_number), (50, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)
            cv2.putText(frame, f'/{frame_count_str} frames', (110, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)
            cv2.putText(frame, f'{fps}/sec', (400, 50), font, 1, (0, 255, 255), 2, cv2.LINE_4)

            # Écrire la frame dans la vidéo de sortie
            video_export.write(frame)
            
            # Affichage CV2
            cv2.imshow('frame', frame)
            if cv2.waitKey(25) & 0xFF == ord('a'):
                break


    """ fin export de la video """
    cap.release() 
    # Closes all the frames 
    cv2.destroyAllWindows() 
    video_export.release() 
    print("The video was successfully saved") 

    """ export du json """
    # Construire le chemin complet pour le fichier de sortie
    output_file_path = os.path.join(os.path.dirname('export-results/json/'), f'{cut_file_name}.json')

    # Écrire les données dans un fichier JSON
    with open(output_file_path, 'w') as f:
        json.dump(data, f, indent=4)