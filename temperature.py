import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import pickle
import sys
import os
import plotly.graph_objects as go

from matplotlib.patches import Polygon
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

def collect_tmpa(data,block):
    
    tmpa = data['block_'+str(block)]['update_history']['alpha']
    entropy = data['block_'+str(block)]['update_history']['entropies']

    return tmpa,entropy


def correct_data(tmps):
    newtmps = []
    # remove every 5th element of the list
    for i in range(len(tmps)):
        if i%5 != 0:
            newtmps.append(tmps[i])
    
    return newtmps

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

if __name__ == '__main__':
    files = os.listdir(sys.argv[1])
    print(sys.argv[2])
    if sys.argv[2] == '1':
        print('hi')
        box_colors = ['#012949','#035CA3', '#088FFA',  '#62B8FC']
        namesc = ['P_NTL_1','P_NTL_2','P_NTL_3','P_NTL_4']
    elif sys.argv[2] == '2':
        box_colors = ['#6D0E10','#BF181D', '#E84B4F', '#F29C9E']
        namesc = ['P_TL_1','P_TL_2','P_TL_3','P_TL_4']
    elif sys.argv[2] == '3':
        box_colors = ['#A8DF8E']
        namesc = ['Temperature','Entropy']
    print(box_colors)
    # if not os.path.exists(sys.argv[2]):
    #     os.makedirs(sys.argv[2])
    p = 0
    # prt(file)
    #fig, ax = plt.subplots(1, 4)
    fig = plt.figure(figsize=(10,4))
    gs = fig.add_gridspec(1, 4, hspace=0.2, wspace=0.2)
    ax = gs.subplots(sharex=True, sharey=True)
    fig.suptitle('Expert')
    for file in files:
        # print(file)
        # #fig, ax = plt.subplots(1, 4)
        # fig = plt.figure(figsize=(10,4))
        # gs = fig.add_gridspec(1, 4, hspace=0.2, wspace=0.2)
        # ax = gs.subplots(sharex=True, sharey=True)
        # fig.suptitle(p_names[file.split('_')[0]])

        for block in range(4):
            
            data = load_data(os.path.join(sys.argv[1],file))
            tmps,entropy = collect_tmpa(data,block)
            
            if len(tmps) == 5000:
                tmps = correct_data(tmps)
            if len(entropy) == 5000:
                entropy = correct_data(entropy)

            ax[block].set_ylim(0,1.4)
            ax[block].plot(tmps,color=box_colors[p],linewidth=2)
            if sys.argv[2] == '3':
                ax[block].plot(entropy,color='#F39F5A',linewidth=0.5)

            ax[block].set_title('OTS '+str(block+1))

            ax[block].set_xlabel('Gradient Updates')
            ax[block].set_ylabel('Value')
            if block == 3:
                ax[block].legend(namesc)
        p+=1
        #save_path = os.path.join(sys.argv[2],file.split('_')[0]+'.png')
    plt.show()
    #plt.savefig(save_path)