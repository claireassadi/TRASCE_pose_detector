import math
import json
import os
import matplotlib.pyplot as plt
import csv
import pandas as pd

def json_to_graph(file_name, figure, point):

    # path of the json file
    json_file_path = f'export-results/json/{file_name}.json'
    csv_file_path = 'export-results/csv/'
    json_file_name = os.path.splitext(os.path.basename(json_file_path))[0]

    # charge the json file
    with open(json_file_path, 'r') as f:
        frames = json.load(f)


    def euclidean_distance(point1, point2):
        """
        Calculate the euclidean distance between to points.
        """
        return math.sqrt((point2["x"] - point1["x"]) ** 2 + (point2["y"] - point1["y"]) ** 2)


    def calculate_distances(frames, figure, point):
        """
        Calculate the euclidean distance of the specified points of each frame.
        """
        distances = []
        num_frames = len(frames)
        for i in range(num_frames - 1):  # check all frame except the last one
            current_frame = frames[i]
            next_frame = frames[i + 1]
            current_figure = current_frame.get(figure, {})
            next_figure = next_frame.get(figure, {})
            
            # Check if specified points is present in the actual figure and the next figure
            if point in current_figure and point in next_figure:
                current_point = current_figure[point]
                next_point = next_figure[point]
                # calculate the euclidean distance between the two points
                distance = euclidean_distance(current_point, next_point)
                distances.append(distance)
            else:
                distances.append(0)  # Add 0 if the point is missing

        return distances



    # export in CSV

    def json_to_csv(distances):
        # Write the distances in a CSV file
        output_csv_file = os.path.join(os.path.dirname(csv_file_path), f'{json_file_name}_{figure}_{point}.csv')

        with open(output_csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Frames', 'Distance'])  # Write column names
            for i in range(len(distances)):
                # Add the frames
                frame_interval = f'{i+1}' if i < len(distances) - 1 else f'{i+1}'
                writer.writerow([frame_interval, distances[i]])

        print(f"The distances are writen in {output_csv_file}.")

    # Function Call
    output_csv_file = os.path.join(os.path.dirname(csv_file_path), f'{json_file_name}_{figure}_{point}.csv')
    output_csv_file_name = os.path.splitext(os.path.basename(output_csv_file))[0]

    # Call of function for calculating the distances for a specified figure
    distances = calculate_distances(frames, figure, point)
    print(f"Distances of points : {point} of each frame for the figure: {figure}")

    # Call of the fucntion to export in CSV
    json_to_csv(distances)

    def graph_distances_frames(frames, distances):

        fig, ax = plt.subplots(figsize=(10, 5))

        df = pd.read_csv(f'{csv_file_path}{output_csv_file_name}.csv')

        frames = df['Frames']
        distances = df['Distance']

        ax.plot(frames, distances, marker='o', color='b', label='Datas')
        ax.plot(frames, distances, linestyle='-', color='r', label='Line')
        ax.set_xlabel('Frames')
        ax.set_ylabel('Distances in pixels')
        ax.set_title(f'Distances in each frames for the figure : {figure} and the point : {point}')
        ax.legend()
        ax.grid(True)

        plt.tight_layout()
        plt.show()

    graph_distances_frames(frames, distances)