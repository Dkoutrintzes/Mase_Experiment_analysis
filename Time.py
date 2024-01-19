import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import pickle
import sys
import os
from matplotlib.patches import Polygon
# Load the data
def load_data(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
        #print(data)
    return data

def collect_average_scores(data):
    scores = []
    done = []
    for i in range(5):
        scores.append(data['block_'+str(i)]['game_score'])
        done.append(data['block_'+str(i)]['done'])
    scores = check_data(scores,done)
    return scores

def save_csv(data, name):
    
    df.to_csv(os.path.join('Csv', name+'.csv'), index=False)


def chart(data):
    sns.boxplot( data=data, palette="Set3")
    

def chart_exp(data,exp_data):
    sns.boxplot( data=data, palette="Set3")
    plt.plot(exp_data, color='red')

def check_data(scores,done):
    for i in range(len(scores)):
        for j in range(len(scores[i])):
            #print(scores[i][j],done[i][j][-1])
            if done[i][j][-1] == False or  scores[i][j] < 20:
                print(scores[i][j],done[i][j][-1])
                scores[i][j] = 0
        
    return scores

if __name__ == '__main__':
    folder =sys.argv[1]
    print('Folder Name: ', folder)
    files = os.listdir(folder)
    data = []
    for file in files:
        p_data = load_data(os.path.join(folder, file) )
        p_scores = collect_average_scores(p_data)
        time_passed = 0
        for block in range(len(p_scores)):
            for game in range(len(p_scores[block])):
                game_time = (200 - p_scores[block][game])/5
                if p_scores[block][game] == 0:
                    game_time += 4
                game_time += 7
                time_passed += game_time
            if block != 4:
                time_passed += 60
        

        data.append(time_passed/60)

    print(data)
        




    plt.show()
