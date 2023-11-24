import matplotlib.pyplot as plt
import dill
from util import *
import numpy as np
import argparse
import pandas as pd



def H_novelty_plot(df):
    with open('result/H-Novelty.pkl', 'rb') as f:
        H_Novelty = dill.load(f)
    
    H_Novelty = list(H_Novelty.values())
    df['H_novelty'] = H_Novelty
    avg_novelty = df[['composer','H_novelty']].groupby('composer').mean()['H_novelty']
    std = []
    for composer in avg_novelty.index:
        c_nov = list(df[df['composer']==composer].H_novelty)
        std.append(jackknife_error(c_nov))
    avg_year = df[['composer','year']].groupby('composer').mean()['year']
    
    fig = plt.figure(figsize=(20,8))
    plt.errorbar(avg_year, avg_novelty, yerr=std, linestyle='none', marker='s', markersize=8, capsize=4)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlabel("Year", fontsize=20)
    plt.ylabel("H-Novelty", fontsize=20)
    for x,y,c in zip(avg_year, avg_novelty, avg_novelty.index):
        plt.text(x+.07, y+.03, c, fontsize=12)
    #plt.show()
    plt.savefig("../figs/H-Novelty plot.jpg")
    


def P_Novelty_plot(df):
    with open('result/P-Novelty.pkl', 'rb') as f:
        P_Novelty = dill.load(f)
    
    avg_novelty = []
    std = []
    composers = df.composer.unique()
    for c in composers:
        nov = P_Novelty[c]
        avg_novelty.append(np.mean(nov))
        std.append(jackknife_error(nov))
    avg_year = list(df[['composer','year']].groupby('composer').mean()['year'])
    
    fig = plt.figure(figsize=(20,8))
    plt.errorbar(avg_year, avg_novelty, yerr=std, linestyle='none', marker='s', markersize=8, capsize=4)
    for x,y,c in zip(avg_year, avg_novelty, composers):
        plt.text(x+2, y+.002, c, fontsize=12)
    #plt.show()
    plt.savefig("../figs/P-Novelty plot.jpg")



def Influence_plot(df, composers_list):
    with open('result/Influence.pkl', 'rb') as f:
        Influence = dill.load(f)

    fig, axes = plt.subplots(1,4,figsize=(20,8))
    periods = [(1710,1750),(1750,1800),(1800,1820),(1820,1950)]
    def get_random_color():
        return tuple(np.random.random(size=3))
    colors = [get_random_color() for i in range(len(composers_list))]
    #colors = ['rebeccapurple','royalblue','palevioletred','lightskyblue','lightgreen','mediumaquamarine','yellow',
    #         'darkorange','crimson','maroon']
    
    for i,composer in enumerate(composers_list):
        influenced_songs = list(Influence[composer].keys())
        influenced_songs_yrs = [metadata['year'][s] for s in influenced_songs]
        smooth_yr_range = [(x-10,x+10) for x in np.arange(min(influenced_songs_yrs), max(influenced_songs_yrs))]
        X = []
        Y = []
        Y_err = []

        for (y1,y2) in smooth_yr_range:
            #print(y1,y2)
            y = [Influence[composer][s] for s in influenced_songs if (metadata['year'][s]>=y1)&(metadata['year'][s]<=y2)]
            if y == []:
                mean_y = 0
                std_y = 0
            else:
                mean_y = np.mean(y)
                std_y = jackknife_error(y)
            
            X.append(np.mean([y1,y2]))
            Y.append(mean_y)
            Y_err.append(std_y)
        
        Y_err = np.array(Y_err)
        
        for j in range(4):
            axes[j].plot(X, Y, c=colors[i], label=composer, markeredgecolor='black', marker='o', linestyle='dashed')
            axes[j].fill_between(X, Y-Y_err/2, Y+Y_err/2, color=colors[i], alpha=0.3)
            axes[j].set_xlim(periods[j][0], periods[j][1])
            if j == 3:
                axes[j].set_xticks(np.arange(periods[j][0], periods[j][1]+1, 30))
            else:
                axes[j].set_xticks(np.arange(periods[j][0], periods[j][1]+1, 10))
            if j in [2,3]:
                axes[j].set_ylim(0,0.1)
    
    axes[-1].legend(fontsize=12)
    #plt.show()
    plt.savefig("../figs/Influence plot.jpg")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--plot', type=str, required=True, help='H-novelty/P-novelty/Influence')
    parser.add_argument('--composers', type=str, help='A list of composers to plot Influence scores', default='Bach, D.Scarlatti, Handel, Haydn, Clementi, Mozart, Beethoven, Schubert, Chopin, Liszt')
    parser.add_argument('--custom_dataset', type=bool, default=False)

    
    args = parser.parse_args()
    composers = [c.strip() for c in args.composers.split(',')] 

    if args.custom_dataset:
        metadata_path = '../data/meta/custom/metadata_custom.csv'
        data_path = '../data/preprocessed/custom/'
    else:
        metadata_path = '../data/meta/novinf/metadata.csv'
        data_path = '../data/preprocessed/novinf/'

    metadata = pd.read_csv(metadata_path, index_col=0)
    
    if args.plot == 'H-novelty':
        H_novelty_plot(df=metadata)
    elif args.plot == 'P-novelty':
        P_Novelty_plot(df=metadata)
    elif args.plot == 'Influence':
        Influence_plot(df=metadata, 
                        composers_list=composers)
