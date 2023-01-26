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
    sns.scatterplot(data=train, y='average_forever', x='initialprice')
    plt.title('Initial Price vs the hours played')
    plt.show
    
# VIZ 1 statistics test
def get_chi_initialprice(train):
    observed = pd.crosstab(train.average_forever, train.initialprice)
    chi2, p, degf, expected = stats.chi2_contingency(observed)
    print(f'chi^2 = {chi2:.4f}')
    print(f'p     = {p:.4f}')
    
# VIZ 2
def developer_visual(train):
    sns.barplot(data=train, y='average_forever', x='Developer_Valve')
    plt.title('Valve developer hours played vs everyone else')
    plt.show
    
# VIZ 2 statistics test
def get_chi_valve(train):
    observed = pd.crosstab(train.average_forever, train.Developer_Valve)
    chi2, p, degf, expected = stats.chi2_contingency(observed)
    print(f'chi^2 = {chi2:.4f}')
    print(f'p     = {p:.4f}')
    
# VIZ 3
def publisher_visual(train):
    sns.barplot(data=train, y='average_forever', x='Publisher_Rockstar_Games')
    plt.title('Valve developer hours played vs everyone else')
    plt.show

# VIZ 3 statistics test
def get_chi_publisher(train):
    observed = pd.crosstab(train.average_forever, train.Publisher_Rockstar_Games)
    chi2, p, degf, expected = stats.chi2_contingency(observed)
    print(f'chi^2 = {chi2:.4f}')
    print(f'p     = {p:.4f}')
    
# VIZ 4
def discount_visual(train):
    sns.barplot(data=train, y='average_forever', x='discount')
    plt.title('Discount vs. Average hours')
    plt.show
    
# VIZ 5
def MMO_visual(train):
    sns.barplot(data=train, y='average_forever', x='Genre_Massively Multiplayer')
    plt.title('MMO vs. Average hours')
    plt.show
    
# VIZ 6
def free_to_play(train):
    sns.barplot(data=train, y='average_forever', x='Price: free_to_play')
    plt.title('Free vs. Average hours')
    plt.show