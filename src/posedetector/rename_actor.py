import json
import os
import tkinter as tk
from tkinter import ttk
from collections import OrderedDict

def rename_actor(file_name):

    # json file path
    json_file_path = f'export-results/json/{file_name}.json'

    nose_x =[]
    nose_y =[]

    def find_nb_keypoints():
        # Charge the json file
        with open(json_file_path, 'r') as f:
            data = json.load(f, object_pairs_hook=OrderedDict)  # Use OrderedDict to have values in order
        
        nb_keypoints = set()  # store unique values
        
        # Loop the data and add the keypoints presents in the json file
        for frame_data in data:
            for i in range(1, len(frame_data)):
                key = list(frame_data.keys())[i]
                value = frame_data[key]
                if isinstance(value, dict):
                    nb_keypoints.add(key)  # Add the name of the keypoint_figure
                    print(list(frame_data.keys())[i])
                    nb_keypoints.add(key)

        # get the values
        nb_keypoints_dict = {keypoint_figure: keypoint_figure for keypoint_figure in nb_keypoints}
        
        return nb_keypoints_dict


    def replace_actor_names(json_file_path, actor_names_mapping):
        # charge the json file
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        
        # loop trought the jsn data to change the keypoint_figure by tne new specified values
        for frame_data in data:
            # Create a copy of data to not modify the original dictionnary
            frame_data_copy = frame_data.copy()
            for key, value in frame_data_copy.items():
                if key in actor_names_mapping:
                    actor_name = actor_names_mapping[key]
                    new_key = actor_name  # Use the new name as the new key
                    frame_data[new_key] = frame_data.pop(key)  # Rename the key with the new name
        
        # Write the data in the json
        with open(json_file_path, 'w') as f:
            json.dump(data, f, indent=4)

    nb_keypoints_dict = find_nb_keypoints()

    def on_submit():
        new_actor_names_mapping = {}
        for key, entry in entries.items():
            new_actor_names_mapping[key] = entry.get()
        replace_actor_names(json_file_path, new_actor_names_mapping)
        print("New name rewriten in the JSON.")
        root.destroy()

    root = tk.Tk()
    root.title("Replace names")

    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    entries = {}
    row = 0
    for key in sorted(nb_keypoints_dict.keys()):  # Tri des clés
        ttk.Label(frame, text=key).grid(row=row, column=0, sticky=tk.W)
        entry = ttk.Entry(frame)
        entry.grid(row=row, column=1, padx=5, pady=5)
        entry.insert(0, nb_keypoints_dict[key])  # Utilisation des valeurs par défaut
        entries[key] = entry
        row += 1

    text = "no space"
    text_label = ttk.Label(frame, text=text)
    text_label.grid(row=row, columnspan=2, pady=10)

    submit_button = ttk.Button(frame, text="Submit", command=on_submit)
    submit_button.grid(row=row+1, columnspan=2)

    root.mainloop()