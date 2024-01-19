import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import pickle
import os
import sys

# Load the data
def load_data(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
        #print(data)
    return data

# Collect scores
def collect_scores(data):
    scores = []
    for i in range(6):
        scores.append(data['block_'+str(i)]['game_score'])
    return scores

def collect_average_scores(data):
    scores = []
    for i in range(6):
        scores.append(np.average(data['block_'+str(i)]['game_score']))
    return scores

# Collect Path
def collect_path(data):
    
    for i in range(6):
        path = []
        x = []
        y = []
        for line in data['block_'+str(i)]['states']:
            for point in line:
                #path.append([point[0], point[1]])
                x.append(point[0])
                y.append(point[1])
        #path.append(data['block_'+str(i)]['states'])
        path.append(x)
        path.append(y)
        plot_path(path)
    return path

# Collect wins
def collect_wins(data):
    wins = []
    for i in range(6):
        print(data['block_'+str(i)]['win_loss'])
        wins.append(data['block_'+str(i)]['win_loss'][0])
        
    return wins

# Collect Travelled distance
def collect_distance(data):
    distance = []
    for i in range(6):
        distance.append(np.average(data['block_'+str(i)]['distance_travel']))
    return distance


# Plot the scores
def plot_scores(scores):
    sns.set_style("darkgrid")
    sns.set_context("talk")
    sns.set_palette("Set2")
    plt.figure(figsize=(10, 5))
    plt.plot(scores)
    plt.xlabel('Block')
    plt.ylabel('Score')
    plt.title('Score per block')
    plt.show()

# Plot the scores with boxplot
def plot_scores_boxplot(scores):
    sns.set_style("darkgrid")
    sns.set_context("talk")
    sns.set_palette("Set2")
    plt.figure(figsize=(10, 5))
    plt.boxplot(scores)
    plt.xlabel('Block')
    plt.ylabel('Score')
    plt.title('Score per block')
    plt.show()

# Plot the path
def plot_path(path):
    sns.set_style("darkgrid")
    sns.set_context("talk")
    sns.set_palette("Set2")
    plt.figure(figsize=(10, 5))
    plt.plot(path[0], path[1])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Path')
    plt.show()

# Plot heatmap
def plot_heatmap(path):
    sns.set_style("darkgrid")
    sns.set_context("talk")
    sns.set_palette("Set2")
    plt.figure(figsize=(10, 5))
    sns.heatmap(path[0], path[1])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Path')
    plt.show()


# Plot wins
def plot_wins(wins):
    sns.set_style("darkgrid")
    sns.set_context("talk")
    sns.set_palette("Set2")
    plt.figure(figsize=(10, 5))
    plt.plot(wins)
    plt.xlabel('Block')
    plt.ylabel('Wins')
    plt.title('Wins per block')
    plt.show()

# Plot distance
def plot_distance(distance):
    sns.set_style("darkgrid")
    sns.set_context("talk")
    sns.set_palette("Set2")
    plt.figure(figsize=(10, 5))
    plt.plot(distance)
    plt.xlabel('Block')
    plt.ylabel('Distance')
    plt.title('Distance per block')
    plt.show()

# Get Accelaration data
def get_acceleration_data(data):
    for i in range(5):
        for line in data['block_'+str(i)]['agent_states'][4]:
            acceleration_x = []
            acceleration_y = []
            
            acceleration_x.append(line['observation'][6])
            acceleration_y.append(line['observation'][7])
            fig = plt.figure()
            ax = fig.add_subplot()
            
            plt.show()



if __name__ == '__main__':
    files = os.listdir(sys.argv[1])
    if not os.path.exists(sys.argv[2]):
        os.mkdir(sys.argv[2])
    for file in files:
        name = file.split('_')[0]
        if not os.path.exists(os.path.join(sys.argv[2], name)):
            os.mkdir(os.path.join(sys.argv[2], name))
        data = load_data(os.path.join(sys.argv[1],file))
        #data = load_data()



        get_acceleration_data(data)