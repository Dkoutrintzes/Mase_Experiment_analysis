import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import pickle
import sys
import os
from matplotlib.patches import Polygon

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

def collect_paths(data,heatmap,block):
        
    for j in range(10):
        path = data['block_'+str(block)]['states'][j]
        x,y = get_path(path)
        heatmap = create_heatmap_array(x,y,20, heatmap)
        
    return heatmap

def get_path(path):
    x = []
    y = []
    for point in path:
        x.append(point[0])
        y.append(point[1])
    return x, y

def classic_heatmap(data,path_to_save,max_value,pname,block):

    plt.figure(figsize=(15,15))
    heat_map = sns.heatmap( data, linewidth = 1,vmin=0, vmax=1 , annot = True, fmt = ".2f", cmap = sns.color_palette("coolwarm", as_cmap=True)
,square=True)
    plt.title( "Participant "+str(pname)+" Block "+str(int(block)+1)+"\nNormileze value {}".format(max_value),fontsize = 40 )
    plt.tick_params(axis='both', which='major', labelsize=10, labelbottom = False, bottom=False, top = True, labeltop=True)

    plt.savefig(path_to_save)


def create_heatmap_array(x,y,size,heatmap):

    #print(heatmap)
    for i in range(len(x)):
        x_temp = float(x[i]) 
        y_temp = float(y[i])

        xn = int((x_temp*(size/4))+(size/2))

        yn = int((y_temp*(size/4))+(size/2))
        #print(xn, yn)
        if xn >= size :
            xn = size-1
        if yn >= size :
            yn = size-1
        if xn < 0 :
            xn = 0
        if yn < 0 :
            yn = 0
        heatmap[yn][xn] += 1

    return heatmap

def convert_heatmap_to_sec(heatmap):
    for i in range(len(heatmap)):
        for j in range(len(heatmap)):
            heatmap[i][j] = heatmap[i][j] / 5
    return heatmap

def find_max_value(heatmap):
    max_value = 0
    for i in range(len(heatmap)):
        for j in range(len(heatmap)):
            if heatmap[i][j] > max_value:
                max_value = heatmap[i][j]
    return max_value

def zeros_to_nan(heatmap):
    for i in range(len(heatmap)):
        for j in range(len(heatmap)):
            if heatmap[i][j] == 0:
                heatmap[i][j] = np.nan
    return heatmap


def normilize_to_max(heatmap,max_value):
    for i in range(len(heatmap)):
        for j in range(len(heatmap)):
            heatmap[i][j] = heatmap[i][j] / max_value
    return heatmap

if __name__ == '__main__':
    files = os.listdir('NO_TL_Final_results')
    #heatmap = np.zeros((20,20))
    #max = 0
    if not os.path.exists('NO_TL_heatmaps'):
        os.mkdir('NO_TL_heatmaps')
    for file in files:
        name = file.split('_')[0]
        if not os.path.exists(os.path.join('NO_TL_heatmaps', name)):
            os.mkdir(os.path.join('NO_TL_heatmaps', name))
        
        data = load_data(os.path.join('NO_TL_Final_results', file) )
        for b in range(5):
            heatmap = np.zeros((20,20))
            name_of_png = name + '_' + str(b) + '.png'
            path_to_save = os.path.join('NO_TL_heatmaps',name, name_of_png)

            heatmap = collect_paths(data,heatmap,b)

            heatmap = convert_heatmap_to_sec(heatmap)
            max_value = find_max_value(heatmap)
            heatmap = normilize_to_max(heatmap,max_value)
            heatmap = zeros_to_nan(heatmap)
            pname = p_names[name]
            classic_heatmap(heatmap,path_to_save,max_value,pname,b)

    
                
    files = os.listdir('TL_Final_results')
    if not os.path.exists('TL_heatmaps'):
        os.mkdir('TL_heatmaps')
    for file in files:
        name = file.split('_')[0]
        if not os.path.exists(os.path.join('TL_heatmaps', name)):
            os.mkdir(os.path.join('TL_heatmaps', name))
        
        data = load_data(os.path.join('TL_Final_results', file) )
        for b in range(5):
            heatmap = np.zeros((20,20))
            name_of_png = name + '_' + str(b) + '.png'
            path_to_save = os.path.join('TL_heatmaps',name, name_of_png)
            
            heatmap = collect_paths(data,heatmap,b)

            heatmap = convert_heatmap_to_sec(heatmap)
            max_value = find_max_value(heatmap)
            heatmap = normilize_to_max(heatmap,max_value)
            heatmap = zeros_to_nan(heatmap)
            pname = p_names[name]
            classic_heatmap(heatmap,path_to_save,max_value,pname,b)

    files = os.listdir('Expert')
    if not os.path.exists('Expert_heatmaps'):
        os.mkdir('Expert_heatmaps')
    for file in files:
        name = file.split('_')[0]
        if not os.path.exists(os.path.join('Expert_heatmaps', name)):
            os.mkdir(os.path.join('Expert_heatmaps', name))
        
        data = load_data(os.path.join('Expert', file) )
        for b in range(5):
            heatmap = np.zeros((20,20))
            name_of_png = name + '_' + str(b) + '.png'
            path_to_save = os.path.join('Expert_heatmaps',name, name_of_png)
            
            heatmap = collect_paths(data,heatmap,b)

            heatmap = convert_heatmap_to_sec(heatmap)
            max_value = find_max_value(heatmap)
            heatmap = normilize_to_max(heatmap,max_value)
            heatmap = zeros_to_nan(heatmap)
            pname = p_names[name]
            classic_heatmap(heatmap,path_to_save,max_value,pname,b)


    #print(max)


        