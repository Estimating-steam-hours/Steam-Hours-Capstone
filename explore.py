import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import os

import sklearn.preprocessing
np.random.seed(123)

import warnings
warnings.filterwarnings("ignore")

from scipy import stats
import re


# VIZ 1
def initial_price(train):
    heavily_played = train[train.binned_hours_explore == 'high_hours']
    heavily_played.binned_release_price.value_counts().plot(kind = 'bar')
    plt.xlabel('Price of Game')
    plt.ylabel('Number of Games')
    plt.xticks(np.arange(3), ['Free to Play', 'Budgeted', 'Full Price'], rotation=0)
    plt.show
    
# Viz 1.b
def price_game(train):
    train.binned_release_price.value_counts().plot(kind = 'bar')
    plt.xlabel('Price of Game')
    plt.ylabel('Number of Games')
    plt.xticks(np.arange(3), ['Free to Play', 'Budgeted', 'Full Price'], rotation=0)
    plt.show
    
# VIZ 1 statistics test
def get_chi_initialprice(train):
    observed = pd.crosstab(train.binned_hours_explore, train.binned_release_price)
    chi2, p, degf, expected = stats.chi2_contingency(observed)
    print(f'chi^2 = {chi2:.4f}')
    print(f'p     = {p:.4f}')
    
# VIZ 2
def developer_visual(train):
    paradox = train[train.Developer_Paradox_Development_Studio == True]
    paradox.binned_hours_explore.value_counts().plot(kind = 'bar')
    plt.title('Distribution of Hours for paradox games')
    plt.xticks(rotation=0)
    plt.show

def supporting_viz(train):
    valve = train[train.Developer_Valve == True]
    valve.binned_hours_explore.value_counts().plot(kind = 'bar')
    plt.xlabel('Hours Played')
    plt.ylabel('Number of Games')
    plt.xticks(np.arange(2), ['Low Hours', 'High Hours'], rotation=0)
    plt.show
    
# VIZ 2 statistics test
def get_chi_valve(train):
    observed = pd.crosstab(train.binned_hours_explore, train.Developer_Valve)
    chi2, p, degf, expected = stats.chi2_contingency(observed)
    print(f'chi^2 = {chi2:.4f}')
    print(f'p     = {p:.4f}')
    
# VIZ 3
def publisher_visual(train):
    rockstar = train[train.Publisher_Rockstar_Games == True]
    rockstar['binned_hours_explore'].value_counts().plot(kind='bar')
    plt.title('Distribution of Rockstar Publisher')
    plt.xticks(rotation=0)
    plt.show
    

# VIZ 3 statistics test
def get_chi_publisher(train):
    observed = pd.crosstab(train.binned_hours_explore, train.Publisher_Rockstar_Games)
    chi2, p, degf, expected = stats.chi2_contingency(observed)
    print(f'chi^2 = {chi2:.4f}')
    print(f'p     = {p:.4f}')
    
# VIZ 4
def discount_visual(train):
    sns.barplot(data=train, y='binned_hours_explore', x='discount')
    plt.title('Discount vs. Average hours')
    plt.xticks(rotation=0)
    plt.show
    
# VIZ 4 statistics test
def get_chi_discount(train):
    observed = pd.crosstab(train.average_forever, train.discount)
    chi2, p, degf, expected = stats.chi2_contingency(observed)
    print(f'chi^2 = {chi2:.4f}')
    print(f'p     = {p:.4f}')
    
# VIZ 5
def MMO_visual(train):
    mmo = train[train['Genre_Massively Multiplayer'] == True]
    mmo['binned_hours_explore'].value_counts().plot(kind='bar')
    plt.xlabel('MMO hours played')
    plt.ylabel('Number of Games')
    plt.xticks(np.arange(2), ['Low Hours', 'High Hours'], rotation=0)
    plt.show
    
# VIZ 6
def free_to_play(train):
    free_to_play = train[train.binned_release_price == 'free_to_play']
    free_to_play.binned_hours_explore.value_counts().plot(kind = 'bar')
    plt.title('free_to_play Distribution Hours')
    plt.xticks(rotation=0)
    plt.show
    
