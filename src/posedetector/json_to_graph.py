import math
import json
import os
import matplotlib.pyplot as plt
import csv
import pandas as pd



def json_to_graph(file_name, figure, point, frame_interval):

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
            
            # Check if specfiad points is present in the actual figure and the next figure
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
            writer.writerow(['Frames', 'Distance'])  # Écriture de l'en-tête
            for i in range(len(distances)):
                # Déterminer l'intervalle de frames
                frame_interval = f'{i+1}:{i+2}' if i < len(distances) - 1 else f'{i+1}'
                writer.writerow([frame_interval, distances[i]])

        print(f"The distances are writen in {output_csv_file}.")


    # Calculating the average values of x and y for each frame batch
    def calculate_xy_mean_batch_frame(frames, figure, point, frame_interval=10):
        x_means = []  # liste for x means values
        y_means = []  # liste for y means values

        num_frames = len(frames)
        print(num_frames)
        for i in range(0, num_frames, frame_interval):
            x_values = []  # liste for x values of each figures
            y_values = []  # liste for y values of each figures

            # Loop each frame in a specified interval
            for j in range(i, min(i + frame_interval, num_frames)):
                frame_data = frames[j]
                figure_data = frame_data.get(figure, {})  # get the values of specified figure
                if point in figure_data:
                    point_data = figure_data[point]  # get the value of the specified point
                    x_values.append(point_data['x'])  # add the value of the x list
                    y_values.append(point_data['y'])  # add the value of the y list
            # Calculate the mean of x and y values of this frame series
            x_mean = sum(x_values) / len(x_values) if x_values else 0
            y_mean = sum(y_values) / len(y_values) if y_values else 0

            # Append the values in the list
            x_means.append(x_mean)
            y_means.append(y_mean)

        return x_means, y_means


    """ Function Call """

    output_csv_file = os.path.join(os.path.dirname(csv_file_path), f'{json_file_name}_{figure}_{point}.csv')
    output_csv_file_name = os.path.splitext(os.path.basename(output_csv_file))[0]

    # Call of function for calculating the distances for a specified figure
    distances = calculate_distances(frames, figure, point)
    print(f"Distances of points : {point} of each frame for the figure: {figure}")


    # Call of the fucntion to export in CSV
    json_to_csv(distances)

    # Call the function to calculate the mean for batches of frame frames
    x_means, y_means = calculate_xy_mean_batch_frame(frames, figure, point)




    def graph_distances_frames(frames, distances, x_means, y_means, frame_interval):
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 5))
        

        #  Charge the data from the CSV
        df = pd.read_csv(f'{csv_file_path}{output_csv_file_name}.csv')

        # Get the values and the distances
        frames = df['Frames']
        distances = df['Distance']

        """ GRAPH 1 """
        ax1.plot(frames, distances, marker='o', color='b', label='Datas')
        ax1.plot(frames, distances, linestyle='-', color='r', label='Line')
        ax1.set_xlabel('Frames')
        ax1.set_ylabel('Distance')
        ax1.set_title(f'Distances in each frames for the figure : {figure} and the point : {point}')
        ax1.legend()
        ax1.grid(True)

        """ GRAPH 2 """
        x = range(0, len(x_means) * frame_interval, frame_interval)
        print(x)
        ax2.plot(x, x_means, label='mean of x values', color='b', marker='o')
        ax2.plot(x, y_means, label='mean of y values', color='r', marker='x')
        ax2.set_title(f'Mean of x and y values for batch of {frame_interval} frames')
        ax2.set_xlabel('Frames')
        ax2.set_ylabel('Mean of values')
        ax2.legend()
        ax2.grid(True)

        plt.tight_layout()
        plt.show()

    graph_distances_frames(frames, distances, x_means, y_means, frame_interval)