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

def box_plot_multiple(data,nb_pt,title,tl=False):
    dists = ['Block 1', 'Block 2', 'Block 3', 'Block 4',
                'Block 5']
    df = []
    for col in range(5):
        temp = []
        for i in range(len(data)):
            df.append(data[i][col])


    fig, ax1 = plt.subplots(figsize=(10, 6))
    fig.canvas.manager.set_window_title('A Boxplot Example')
    fig.subplots_adjust(left=0.075, right=0.95, top=0.9, bottom=0.25)
    pos = []
    space_bx = 1
    ext_space = 0
    for i in range(len(df)):
        pos.append(space_bx)
        if (i+1)%nb_pt == 0:
            ext_space = 0.5
        else:
            ext_space = 0
        space_bx += 1 + ext_space
    print(pos)
    bp = ax1.boxplot(df, notch=False, sym='+', vert=True, whis=1,positions=pos)
    plt.setp(bp['boxes'], color='black')
    plt.setp(bp['whiskers'], color='black')
    plt.setp(bp['fliers'], color='red', marker='+')

    # Add a horizontal grid to the plot, but make it very light in color
    # so we can use it for reading data values but not be distracting
    ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey',
                alpha=0.5)

    ax1.set(
        axisbelow=True,  # Hide the grid behind plot objects
        title=title,
        xlabel='Blocks',
        ylabel='Scores Per Game',
    )

    # Now fill the boxes with desired colors
    #box_colors = ['indianred','darkkhaki', 'royalblue', 'violet', 'cyan']
    if tl == False:
        #No TL
        #box_colors = ['#526D82','#E966A0', '#6C00FF', '#B70404', '#F97B22']
        box_colors = ['#A8DF8E','#012949','#035CA3', '#088FFA',  '#62B8FC']
    elif tl == True:
            # TL
        #box_colors = ['#526D82',"#C539B4",'#F9F54B','#00FFCA','#539165']
        box_colors = ['#A8DF8E','#6D0E10','#BF181D', '#E84B4F', '#F29C9E']
    num_boxes = len(df)
    medians = np.empty(num_boxes)
    for i in range(num_boxes):
        box = bp['boxes'][i]
        box_x = []
        box_y = []
        for j in range(5):
            box_x.append(box.get_xdata()[j])
            box_y.append(box.get_ydata()[j])
        box_coords = np.column_stack([box_x, box_y])
        
        # Alternate between Dark Khaki and Royal Blue
        ax1.add_patch(Polygon(box_coords, facecolor=box_colors[i % nb_pt]))

        # Now draw the median lines back over what we just filled in
        med = bp['medians'][i]
        median_x = []
        median_y = []
        for j in range(2):
            median_x.append(med.get_xdata()[j])
            median_y.append(med.get_ydata()[j])
            ax1.plot(median_x, median_y, 'k')
        medians[i] = median_y[0]
        # Finally, overplot the sample averages, with horizontal alignment
        # in the center of each box
        # ax1.plot(np.average(med.get_xdata()), np.average(df[i]),
        #         color='w', marker='*', markeredgecolor='k')

    # Set the axes ranges and axes labels
    ax1.set_xlim(0.5, num_boxes + (nb_pt * 0.5)+ 0.5)
    top = 200
    bottom = 0
    ax1.set_ylim(bottom, top)
    #ax1.set_xticklabels(np.repeat(dists, nb_pt),
    #                   rotation=45, fontsize=8)
    ax1.set_xticklabels([' ',' ','1st',' ',' ',' ',' ','2nd',' ',' ',' ',' ','3rd',' ',' ',' ',' ','4th',' ',' ',' ',' ','5th',' ',' '], rotation=45, fontsize=8)

    # Due to the Y-axis scale being different across samples, it can be
    # hard to compare differences in medians across the samples. Add upper
    # X-axis tick labels with the sample medians to aid in comparison
    # (just use two decimal places of precision)
    #pos = np.arange(num_boxes) + 1
    upper_labels = [str(round(s, nb_pt)) for s in medians]
    weights = ['bold','semibold','bold', 'semibold','bold', 'semibold']
    for tick, label in zip(range(num_boxes), ax1.get_xticklabels()):
        k = tick % nb_pt
        ax1.text(pos[tick], .95, upper_labels[tick],
                transform=ax1.get_xaxis_transform(),
                horizontalalignment='center', size='x-small',
                weight=weights[k], color=box_colors[k])
    if tl == False:
        nm = ['P_NTP_1','P_NTP_2','P_NTP_3','P_NTP_4','P_NTP_5']
    elif tl == True:
        nm = ['P_TP_1','P_TP_2','P_TP_3','P_TP_4','P_TP_5']
    # Finally, add a basic legend
    space = 0.035
    fig.text(0.70, 0.12 , f'Expert', color='black', weight='roman',
                size='x-small')
    fig.text(0.75, 0.12, "  ", backgroundcolor=box_colors[0],
                color='black', weight='roman',
                size='x-small')
    for i in range(nb_pt-1):
        fig.text(0.80, 0.12 - (i * space), f'{nm[i]}',
                color='black', weight='roman',
                size='x-small')
        fig.text(0.85, 0.12 - (i * space), "  ", backgroundcolor=box_colors[i+1],
                color='black', weight='roman',
                size='x-small')

    
    # fig.text(0.90, 0.015, '*', color='white', backgroundcolor='silver',
    #      weight='roman', size='medium')
    # fig.text(0.915, 0.013, ' Avg Value', color='black', weight='roman',
    #         size='x-small')

    plt.show()

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
    data.append(collect_average_scores(load_data(os.path.join('Expert',os.listdir('Expert')[0] ))))
    for file in files:
        print(file)
        data.append(collect_average_scores(load_data(os.path.join(folder, file) )))
        print(data)
        
    box_plot_multiple(data,5,'No Transfer Learning Group',False)
    #df = pd.DataFrame(data, columns=['Block 1', 'Block 2', 'Block 3', 'Block 4', 'Block 5'])
    #print(df)
    #save_csv(df, sys.argv[2])

    #chart(df)

    exp_data = collect_average_scores(load_data(os.path.join('Expert',os.listdir('Expert')[0] )))

    #chart_exp(df, exp_data)

    plt.show()
