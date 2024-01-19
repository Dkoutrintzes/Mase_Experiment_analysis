import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import pickle
import sys
import os
import plotly.graph_objects as go

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

def collect_paths(data,block,game):
    
    path = data['block_'+str(block)]['states'][game]
    #x,y = get_path(path)
    x,y,vel = get_path_with_vel(path)


        
    return x,y,vel

def get_wins(data,block):
    wins = data['block_'+str(block)]['win_loss'][0]
    return wins

def get_path(path):
    x = []
    y = []
    for point in path:
        x.append(point[0])
        y.append(point[1])
    return x, y

def get_path_with_vel(path):
    x = []
    y = []
    vel = []
    for point in path:
        x.append(point[0])
        y.append(-point[1])
        velocity = np.sqrt(point[2]**2 + point[3]**2)
        vel.append(velocity)
    return x, y, vel

def classic_heatmap(data,path_to_save,max_value):
    # 2. Generate a 10x10 random integer matrix
    
    
    #print("Our dataset is : ",data)
    
    # 3. Plot the heatmap
    plt.figure(figsize=(15,15))
    heat_map = sns.heatmap( data, linewidth = 1,vmin=0, vmax=1 , annot = True, fmt = ".2f", cmap = sns.color_palette("coolwarm", as_cmap=True)
,square=True)
    plt.title( "Normilezed for maximum value of {}".format(max_value) )
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

def find_start(heatmap):
    for i in range(len(heatmap)):
        for j in range(len(heatmap)):
            if heatmap[i][j] == 0:
                return i,j

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


def add_arrow(line, position=None, direction='right', size=15, color=None):
    """
    add an arrow to a line.

    line:       Line2D object
    position:   x-position of the arrow. If None, mean of xdata is taken
    direction:  'left' or 'right'
    size:       size of the arrow in fontsize points
    color:      if None, line color is taken.
    """
    if color is None:
        color = line.get_color()

    xdata = line.get_xdata()
    ydata = line.get_ydata()

    if position is None:
        position = xdata.mean()
    # find closest index
    start_ind = np.argmin(np.absolute(xdata - position))
    if direction == 'right':
        end_ind = start_ind + 1
    else:
        end_ind = start_ind - 1

    line.axes.annotate('',
        xytext=(xdata[start_ind], ydata[start_ind]),
        xy=(xdata[end_ind], ydata[end_ind]),
        arrowprops=dict(arrowstyle="-|>", color=color),
        size=size
    )


def plot_paths(fig,ax,paths):
    
    line = plt.plot(paths[0],paths[1])[0]
    for f in range(len(paths[0])):
        # every 20 steps
        if f % 5 == 0:
            if f+1 < len(paths[0])-1:    
                add_arrow(line,position=paths[0][f],direction='right',size=10)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)

    ax.set_aspect('equal', adjustable='box')
    #plt.show()
    return fig,ax
    


if __name__ == '__main__':
    files = os.listdir(sys.argv[1])
    if not os.path.exists(sys.argv[2]):
        os.mkdir(sys.argv[2])
    for file in files:
        name = file.split('_')[0]
        if not os.path.exists(os.path.join(sys.argv[2], name)):
            os.mkdir(os.path.join(sys.argv[2], name))
        data = load_data(os.path.join(sys.argv[1],file))
        for block in range(5):
            fig = plt.figure()
            ax = fig.add_subplot()
            ax.set_aspect('equal', adjustable='box')
            ax.set_xlim(-2.1,2.1)
            ax.set_ylim(-2.1,2.1)
            for game in range(10):
                x,y,vel = collect_paths(data,block,game)
                fig,ax = plot_paths(fig,ax,[x,y])
            wins = get_wins(data,block)
            ax.set_title("Participant: "+str(p_names[name])+"  Block: {}".format(block+1)+ " \nWins in this block: {}".format(wins))
            #plt.show()
            fig.savefig(os.path.join(sys.argv[2],name,'Block_'+str(block)+'.png'))
                
    
   

    

    # heatmap_top_left = np.zeros((15,15))
    # heatmap_top_right = np.zeros((15,15))
    # heatmap_bottom_right = np.zeros((15,15))

    # top_left = []
    # top_right = []
    # bottom_right = []
    # figbottom_right = []
    # figtop_right = []
    # figtop_left = []

    # for i in range(10):

    #     x,y,vel = collect_paths(data,sys.argv[3],i)
    # #     max_vel = max(vel)
    # #     step = max_vel / 6
    # #     print(max_vel,step)

    # #     palette = list(reversed(sns.color_palette("Spectral").as_hex()))
    # #     print(palette)
    # #     colors = []
    # #     for j in range(len(vel)):
    # #         if vel[j] < step:
    # #             colors.append(palette[0])
    # #         elif vel[j] < step*2:
    # #             colors.append(palette[1])
    # #         elif vel[j] < step*3:
    # #             colors.append(palette[2])
    # #         elif vel[j] < step*4:
    # #             colors.append(palette[3])
    # #         elif vel[j] < step*5:
    # #             colors.append(palette[4])
    # #         else:
    # #             colors.append(palette[5])

    # #     for l in range(len(y)):
    # #         y[l] = -y[l]
    #     x_start = round(x[0])
    #     y_start = round(y[0])





    # #     # palette = list(reversed(sns.color_palette("Spectral").as_hex()))
    # #     # print(palette)
    # #     # print(vel)

    # #     # # create trace
    # #     # trace = go.Scatter(
    # #     #     x=x, 
    # #     #     y=y, 
    # #     #     mode='markers+lines', 
    # #     #     marker={'color': colors}, 
    # #     #     line={'color': 'gray'}
    # #     # )

    # #     # # crate figure, plot 
    # #     # fig = go.Figure(data=trace)
    # #     # fig.show()
    # #     # break


    #     if x_start == -1 and y_start == 2:
    #         print("Top Left",x_start,y_start)
    #         figtop_left.append([x,y])
    #     elif x_start == 2 and y_start == 2:
    #         print("Top Right",x_start,y_start)
    #         figtop_right.append([x,y])
    #     elif x_start == 2 and y_start == -1:
    #         print("Bottom Right",x_start,y_start)
    #         figbottom_right.append([x,y])







    #     x_start = round(x[0])
    #     y_start = round(y[0])
    #     print(x_start,y_start)
    #     if x_start == -1 and y_start == 2:
    #         print("Top Left",x_start,y_start)
    #         bottom_right.append([x,y])
    #         heatmap_bottom_right = create_heatmap_array(x,y,15,heatmap_bottom_right)
    #     elif x_start == 2 and y_start == 2:
    #         print("Top Right",x_start,y_start)
    #         top_right.append([x,y])
    #         heatmap_top_right = create_heatmap_array(x,y,15,heatmap_top_right)
    #     elif x_start == 2 and y_start == -1:
    #         print("Bottom Right",x_start,y_start)
    #         top_left.append([x,y])
    #         heatmap_top_left = create_heatmap_array(x,y,15,heatmap_top_left)

    # if os.path.exists('Test') == False:
    #     os.mkdir('Test')
    # if os.path.exists(os.path.join('Test',sys.argv[2])) == False:
    #     os.mkdir(os.path.join('Test',sys.argv[2]))
    
    # # path_to_save = os.path.join('Test',sys.argv[2], 'Bot_Right.png')
    # # convert_heatmap_to_sec(heatmap_bottom_right)
    # # mv = find_max_value(heatmap_bottom_right)
    # # heatmap_bottom_right = normilize_to_max(heatmap_bottom_right,mv)
    # # heatmap_bottom_right = zeros_to_nan(heatmap_bottom_right)

    # # classic_heatmap(heatmap_bottom_right,path_to_save,mv)

    # # path_to_save = os.path.join('Test',sys.argv[2], 'Top_Right.png')
    # # convert_heatmap_to_sec(heatmap_top_right)
    # # mv = find_max_value(heatmap_top_right)
    # # heatmap_top_right = normilize_to_max(heatmap_top_right,mv)
    # # heatmap_top_right = zeros_to_nan(heatmap_top_right)
    # # classic_heatmap(heatmap_top_right,path_to_save,mv)

    # # path_to_save = os.path.join('Test',sys.argv[2], 'Top_Left.png')
    # # convert_heatmap_to_sec(heatmap_top_left)
    # # mv = find_max_value(heatmap_top_left)
    # # heatmap_top_left = normilize_to_max(heatmap_top_left,mv)
    # # heatmap_top_left = zeros_to_nan(heatmap_top_left)
    # # classic_heatmap(heatmap_top_left,path_to_save,mv)


    # fig = plt.figure()
    # ax = fig.add_subplot()
    # for i in range(len(figbottom_right)):
    #     line = plt.plot(figbottom_right[i][0],figbottom_right[i][1])[0]
    #     for f in range(len(figbottom_right[i][0])):
    #         # every 20 steps
    #         if f % 5 == 0:
    #             add_arrow(line,position=figbottom_right[i][0][f],direction='right',size=10)
    # ax.axes.xaxis.set_visible(False)
    # ax.axes.yaxis.set_visible(False)

    # ax.set_aspect('equal', adjustable='box')
    # plt.show()


    # fig = plt.figure()
    # ax = fig.add_subplot()
    # for i in range(len(figtop_right)):

    #     plt.plot(figtop_right[i][0],figtop_right[i][1])
    # ax.axes.xaxis.set_visible(False)
    # ax.axes.yaxis.set_visible(False)

    # ax.set_aspect('equal', adjustable='box')
    # plt.show()


    # fig = plt.figure()
    # ax = fig.add_subplot()
    # for i in range(len(figtop_left)):
    #     plt.plot(figtop_left[i][0],figtop_left[i][1])
    # ax.axes.xaxis.set_visible(False)
    # ax.axes.yaxis.set_visible(False)

    # ax.set_aspect('equal', adjustable='box')
    # plt.show()

    


    





        