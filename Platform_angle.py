import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import pickle
import sys
import os
from matplotlib.patches import Polygon
import random


p_names = {
    'DyK2': 'Expert',
    'SXS': 'P_NTL_4',
    'PXX': 'P_NTL_3',
    'MXA': 'P_NTL_1',
    'OXK': 'P_NTL_2',
    'NXT': 'P_TL_3',
    'EXP': 'P_TL_2',
    'NXX': 'P_TL_4',
    'BXM': 'P_TL_1',

}


# Load the data
def load_data(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
        #print(data)
    return data

def collect_average_scores(data):
    scores = []
    for i in range(5):
        scores.append(data['block_'+str(i)]['game_score'])
    return scores

def collect_paths(data,name,savepath):
    
    fig = plt.figure(figsize=(15, 10))
    axt = [311, 312, 313]
    blocks = [0,2,4]
    for j in range(3):
        game = random.randint(0, 9)
        states = data['block_'+str(blocks[j])]['states'][game]
        x,y = get_angle(states)
        #fig = plt.figure(figsize=(15, 5))
        
        print(axt[j])
        ax = fig.add_subplot(axt[j])
        #ax.set_xlim(-3,3)
        ax.set_ylim(-3,3)
            
        ax.set_title('Block '+str(blocks[j]+1) + ' Game '+str(game+1))
        if blocks[j] == 4:
            ax.set_xlabel('Iterations')
        #ax.set_xlabel('Iterations')
        ax.plot(x,marker='o',linestyle='dashed',linewidth=1, markersize=4)
        ax.plot(y,marker='o',linestyle='dashed',linewidth=1, markersize=4)
        x,y = get_pos_inputs(states)
        ax.scatter(y,x,s=2, color = 'green')
        x,y = get_neg_inputs(states)
        ax.scatter(y,x,s=2, color = 'red')
        if j == 0:
            ax.legend(['Agents Tray angle', 'PT Tray angle', 'PT Positive inputs', 'PT Negative inputs'], loc='upper left')  
    #fig.tight_layout(pad=7.0)
    #plt.subplots_adjust(top=0.9)
    fig.suptitle(p_names[name])
    
    plt.savefig(os.path.join(savepath, name+'.png'))         
            
            
    

def get_angle(states):
    x = []
    y = []
    for point in states:
        x.append(point[4]/10)
        y.append(point[5]/10)
    return x, y

def get_pos_inputs(states):
    x = []
    y = []
    i = 0
    for point in states:
        if point[7] > 0:
            x.append(1)
            y.append(i)
        i += 1
    return x,y
def get_neg_inputs(states):
    x = []
    y = []
    i = 0
    for point in states:
        if point[7] < 0:
            x.append(-1)
            y.append(i)
        i += 1
    return x,y

if __name__ == '__main__':
    files = os.listdir(sys.argv[1])
    heatmap = np.zeros((10,10))
    for file in files:
        data = load_data(os.path.join(sys.argv[1], file) )
        savepath = os.path.join(sys.argv[2])
        if not os.path.exists(savepath):
            os.makedirs(savepath)

        collect_paths(data, file.split('_')[0], savepath)

        

    