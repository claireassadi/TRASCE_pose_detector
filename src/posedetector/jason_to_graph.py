import math
import json
import os
import matplotlib.pyplot as plt
import csv
import pandas as pd

# Chemin du fichier JSON
json_file_path = 'runs/pose/json/mini_zaina480p.json'
file_name = os.path.splitext(os.path.basename(json_file_path))[0]

# Charger le fichier JSON
with open(json_file_path, 'r') as f:
    frames = json.load(f)


# Distance euclidienne
def euclidean_distance(point1, point2):
    """
    Calcule la distance euclidienne entre deux points.
    """
    return math.sqrt((point2["x"] - point1["x"]) ** 2 + (point2["y"] - point1["y"]) ** 2)


# Calcul de la distance euclidienne sur tous les points spécifiées
def calculate_distances(frames, figure, point):
    """
    Calcule la distance euclidienne entre les points spécifiés de chaque frame.
    """
    distances = []
    num_frames = len(frames)
    for i in range(num_frames - 1):  # Parcourir toutes les frames sauf la dernière
        current_frame = frames[i]
        next_frame = frames[i + 1]
        current_figure = current_frame.get(figure, {})
        next_figure = next_frame.get(figure, {})
        
        # Vérifier si le point spécifié est présent dans la figure actuelle et la figure suivante
        if point in current_figure and point in next_figure:
            current_point = current_figure[point]
            next_point = next_figure[point]
            # Calculer la distance euclidienne entre les points
            distance = euclidean_distance(current_point, next_point)
            distances.append(distance)
        else:
            distances.append(0)  # Ajouter 0 si le point n'est pas présent

    return distances



# export en CSV

def json_to_csv(distances):
    # Écrire les distances dans un fichier CSV
    output_csv_file = os.path.join(os.path.dirname('runs/pose/csv/'), f'{file_name}.csv')

    with open(output_csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Frames', 'Distance'])  # Écriture de l'en-tête
        for i in range(len(distances)):
            # Déterminer l'intervalle de frames
            frame_interval = f'{i+1}:{i+2}' if i < len(distances) - 1 else f'{i+1}'
            writer.writerow([frame_interval, distances[i]])

    print(f"Les distances ont été enregistrées dans {output_csv_file}.")


# Calcul de la moyenne des valeurs x et y pour chaque tranche de frames
def calculate_xy_mean_batch_frame(frames, figure, point, frame_interval=10):
    x_means = []  # Liste pour stocker les moyennes des valeurs x
    y_means = []  # Liste pour stocker les moyennes des valeurs y

    num_frames = len(frames)
    print(num_frames)
    for i in range(0, num_frames, frame_interval):
        x_values = []  # Liste pour stocker les valeurs x pour chaque figure
        y_values = []  # Liste pour stocker les valeurs y pour chaque figure

        # Parcourir chaque frame dans l'intervalle spécifié
        for j in range(i, min(i + frame_interval, num_frames)):
            frame_data = frames[j]
            figure_data = frame_data.get(figure, {})  # Obtenir les données de la figure spécifiée
            if point in figure_data:
                point_data = figure_data[point]  # Obtenir les données du point spécifié dans la figure
                x_values.append(point_data['x'])  # Ajouter la valeur x du point à la liste
                y_values.append(point_data['y'])  # Ajouter la valeur y du point à la liste

        # Calculer la moyenne des valeurs x et y pour cette série de frames
        x_mean = sum(x_values) / len(x_values) if x_values else 0
        y_mean = sum(y_values) / len(y_values) if y_values else 0

        # Ajouter les moyennes calculées aux listes respectives
        x_means.append(x_mean)
        y_means.append(y_mean)

    return x_means, y_means


""" APPPEL DES FONCTIONS """

figure = "keypoints_figure_1"
point = "right_wrist"
frame_interval=10

# Appel de la fonction pour calculer les distances avec la prise en compte du keypoint_figure_4
distances = calculate_distances(frames, figure, point)
print(f"Distances entre les points {point} de chaque frame de la figure {figure}:")


# Appel de la fonction pour exporter les données en CSV
json_to_csv(distances)

# Appel de la fonction pour calculer les moyennes sur chaque tranche de 10 frames
x_means, y_means = calculate_xy_mean_batch_frame(frames, figure, point)




def graph_distances_frames(frames, distances, x_means, y_means, frame_interval):
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 5))
    
    """ GRAPH 1 """

    # Charger les données depuis le fichier CSV
    df = pd.read_csv(f'runs/pose/csv/{file_name}.csv')

    # Extraire les valeurs de frame et de distance
    frames = df['Frames']
    distances = df['Distance']

    # Graphique 1 : Courbe lisse des distances
    ax1.plot(frames, distances, marker='o', color='b', label='Données brutes')
    ax1.plot(frames, distances, linestyle='-', color='r', label='Courbe lisse')
    ax1.set_xlabel('Frames')
    ax1.set_ylabel('Distance')
    ax1.set_title(f'Courbe lisse des distances en fonction des frames de la personne : {figure} et du point : {point}')
    ax1.legend()
    ax1.grid(True)

    """ GRAPH 2 """

    # Graphique 2 : Moyenne des valeurs x et y pour chaque tranche de frames
    x = range(0, len(x_means) * frame_interval, frame_interval)  # Axe x : pas de frame
    print(x)
    ax2.plot(x, x_means, label='Moyenne des valeurs x', color='b', marker='o')
    ax2.plot(x, y_means, label='Moyenne des valeurs y', color='r', marker='x')
    ax2.set_title(f'Moyenne des valeurs x et y pour chaque tranche de {frame_interval} frames')
    ax2.set_xlabel('Frames')
    ax2.set_ylabel('Moyenne des valeurs')
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()
    plt.show()

graph_distances_frames(frames, distances, x_means, y_means, frame_interval)