import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np
import pickle

import os

# Load the data
def load_data(path):
    with open(path, 'rb') as f:
        data = pickle.load(f)
        #print(data)
    return data


def collect_average_scores(data):
    scores = []
    for i in range(1):
        scores.append(np.average(data['block_'+str(i)]['game_score']))
    return scores


if __name__ == '__main__':
    files = os.listdir('test')

    scores = []
    avg = 0
    for file in files:
        data = load_data(os.path.join('test', file) )
        score = collect_average_scores(data)

        name = file.split('_')[0]

        scores.append([float(score[0]), float(name)])
        avg += float(score[0])

    avg = avg/len(files)
    print(avg)
    
    print(scores)
    scores = np.array(scores)
    sortedArr = scores[scores[0,:].argsort()]
    print(scores)
    # files = os.listdir('NO_TL_Random_results')
    # #file = files[0]
    # for file in files:
    #     data = load_data(os.path.join('NO_TL_Random_results', file) )
    #     print(os.path.join('NO_TL_Random_results', file))
    #     print(data)


    

