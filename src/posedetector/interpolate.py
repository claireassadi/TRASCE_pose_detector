import json
import os

def interpolate_missing_values(file_name):
    json_file_path = f'export-results/json/{file_name}.json'
    # charge the json file
    with open(json_file_path, 'r') as f:
        data = json.load(f)

    # check all actors
    for person_name in data[0].keys():
        # check if actor has keypoints
        if person_name != 'frame':
            # loop trought all actor keypoints
            for keypoint_name in data[0][person_name].keys():
                # loop in each frame
                for i in range(len(data)):
                    keypoint_data = data[i][person_name][keypoint_name]

                    # check if x and y hav missing values
                    if keypoint_data['x'] == 0.0 or keypoint_data['y'] == 0.0:
                        # find the frame before without missing values
                        j = i - 1
                        while j >= 0 and (data[j][person_name][keypoint_name]['x'] == 0.0 or data[j][person_name][keypoint_name]['y'] == 0.0):
                            j -= 1

                        if j >= 0:
                            # find the frame after without missing values
                            k = i + 1
                            while k < len(data) and (data[k][person_name][keypoint_name]['x'] == 0.0 or data[k][person_name][keypoint_name]['y'] == 0.0):
                                k += 1

                            if k < len(data):
                                # interpolate taking the mean of the value of the frame before and after
                                interpolated_value_x = (data[j][person_name][keypoint_name]['x'] + data[k][person_name][keypoint_name]['x']) / 2
                                interpolated_value_y = (data[j][person_name][keypoint_name]['y'] + data[k][person_name][keypoint_name]['y']) / 2
                                # Change the value of the actual frame
                                keypoint_data['x'] = interpolated_value_x
                                keypoint_data['y'] = interpolated_value_y
                            else:
                                # if no value is found after, interpolate with the values before
                                keypoint_data['x'] = data[j][person_name][keypoint_name]['x']
                                keypoint_data['y'] = data[j][person_name][keypoint_name]['y']
                        else:
                            # if no value is found before, interpolate with the values after
                            k = i + 1
                            while k < len(data) and (data[k][person_name][keypoint_name]['x'] == 0.0 or data[k][person_name][keypoint_name]['y'] == 0.0):
                                k += 1

                            if k < len(data):
                                keypoint_data['x'] = data[k][person_name][keypoint_name]['x']
                                keypoint_data['y'] = data[k][person_name][keypoint_name]['y']

    # Export the values in the json file
    output_directory = 'export-results/json/'
    os.makedirs(output_directory, exist_ok=True)
    cut_file_name = os.path.splitext(os.path.basename(json_file_path))[0]
    output_file_path = os.path.join(output_directory, f'{cut_file_name}.json')

    # write the values in the json file
    with open(output_file_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"The data are exported : {output_file_path}")