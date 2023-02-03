import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import os
import requests

#Creating list of top 10 publishers from https://learn.g2.com/video-game-publishers

AAA = ['Tencent Games','Sony Interactive','Microsoft','Activision Blizzard','Electronic Arts','Nintendo','Bandai Namco','Take-Two Interactive','Ubisoft','Square Enix']

#Creating a list of top 10 indie publishers from https://ninichimusic.com/blog/16-indie-friendly-indie-game-publishers

III = ['Curve Digital','Ukuza','Team 17','Devolver Digital','Indie Fund','Midnight City','Serenity Forge','Noodlecake Studios','Versus Evil','Mode 7 Games']


def clean_steamspy(df):
    
    #Turning minutes to hours
    df.iloc[:,[9,10,11,12]] = (df.iloc[:,[9,10,11,12]] / 60)
    #df = df[df['average_forever']!=0]
    #BINS FOR TARGET
    ninety = np.quantile(df['average_forever'], 0.90)
    ten = np.quantile(df['average_forever'], 0.10)
    IQR = ninety - ten
    target_bins_explore = [0,73.146,1000]
    target_labels_explore = ['low_hours','high_hours']
    df['binned_hours_explore'] = pd.cut(df['average_forever'], bins = target_bins_explore, labels = target_labels_explore)
    target_bins = [0,73.146,1000]
    target_labels = [ 0, 1]
    df['binned_hours'] = pd.cut(df['average_forever'], bins = target_bins, labels = target_labels)

    #Drops
    df = df.drop(columns = ['score_rank','userscore'])
    df = df.dropna()
    

    #BINS FOR RELEASE PRICE
    price_bins = [-1,2000,4000,100000]
    price_labels = ['free_to_play','budget_games','full_price_games']
    df['binned_release_price'] = pd.cut(df['initialprice'], bins = price_bins, labels = price_labels)
    df['free_to_play'] = df.binned_release_price == 'free_to_play'
    df['budget_games'] = df.binned_release_price == 'budget_games'
    df['full_price'] = df.binned_release_price == 'full_price_games'

    #formatting pub and dev strings
    df.publisher = df.publisher.str.replace(' ', '_')
    df.developer = df.developer.str.replace(' ','_')
    df = df[df.average_forever > 0]
#PUBLISHER ENCODING:
    Publisher_list = ['']
    word = ''
    for x in df.publisher[(df.binned_hours_explore == 'high_hours') & (df.owners != '0 .. 20,000') & (df.owners != '20,000 .. 50,000') & (df.owners != '50,000 .. 100,000') & (df.owners != '100,000 .. 200,000') & (df.owners != '200,000 .. 500,000') & (df.owners != '500,000 .. 1,000,000')].tolist():
        for a in str(x):
            if a != ',':
                word = word + a
            else:
                if word not in Publisher_list:
                    Publisher_list.append(word)
                    word = ''
                word = ''
        if word not in Publisher_list:
            Publisher_list.append(word)
            word = ''
        word = ''
    for x in Publisher_list:
        x = x.replace(' ','_')
    for x in Publisher_list:
        df[f'Publisher_{x}'] = df.publisher.str.contains(x,regex = False)
#Developer Encoding
    Developer_list = ['']
    word = ''
    for x in df.developer[(df.binned_hours_explore == 'high_hours') & (df.owners != '0 .. 20,000') & (df.owners != '20,000 .. 50,000') & (df.owners != '50,000 .. 100,000') & (df.owners != '100,000 .. 200,000') & (df.owners != '200,000 .. 500,000') & (df.owners != '500,000 .. 1,000,000')].tolist():
        for a in str(x):
            if a != ',':
                word = word + a
            else:
                if word not in Developer_list:
                    Developer_list.append(word)
                    word = ''
                word = ''
        if word not in Developer_list:
            Developer_list.append(word)
            word = ''
        word = ''
    for x in Developer_list:
        x = x.replace(' ','_')
    for x in Developer_list:
        df[f'Developer_{x}'] = df.developer.str.contains(x,regex = False)
    df['Developer_other'] = df.developer.str not in Developer_list
#GENRE ENCODING:
### FINDS UNIQUE WORDS FROM LIST OF GENRES
    genre_list = []
    word = ''
    for x in df.genre.tolist():
        for a in str(x):
            if a != ',':
                word = word + a
            else:
                if word not in genre_list:
                    genre_list.append(word)
                    word = ''
                word = ''
        if word not in genre_list:
            genre_list.append(word)
            word = ''
        word = ''
    for x in genre_list:
        x = x.replace(' ','_')
    for x in genre_list:
        df[f'Genre_{x}'] = df.genre.str.contains(x)




    return df

def scale_numeric(df):
    df.iloc[:,[6,7,8,9,10]] = scaler.fit_transform(df.iloc[:,[6,7,8,9,10]])
    return df
def my_train_test_split(df):

    train, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train, test_size=.25, random_state=123)

    return train, validate, test

def get_steamspy_all():
    '''
    This function checks if device has required csv to run project.
    If not, requests data from steamspy to create csv.
    '''
    if os.path.isfile('steamspy_3000_games.csv'):

        # If csv file exists read in data from csv file.
        df = pd.read_csv('steamspy_3000_games.csv', index_col=0)

        app_list = list(df.appid)

    else:
        #Begin pulling data from steamspy
        long_response1 = requests.get('https://steamspy.com/api.php?request=all&page=0')
        long_data1 = long_response1.json()
        steamspy_df1 = pd.DataFrame(long_data1).T

        long_response2 = requests.get('https://steamspy.com/api.php?request=all&page=1')
        long_data2 = long_response2.json()
        steamspy_df2 = pd.DataFrame(long_data2).T

        long_response3 = requests.get('https://steamspy.com/api.php?request=all&page=2')
        long_data3 = long_response3.json()
        steamspy_df3 = pd.DataFrame(long_data3).T

        frames = [steamspy_df1, steamspy_df2, steamspy_df3]
        df = pd.concat(frames)

        df.to_csv('steamspy_3000_games.csv')

        app_list = list(df.appid)

    return df, app_list

def get_tags_genre(app_list):
    '''
    This function checks if device has required csv to run project.
    If not, requests data from steamspy to create csv.
    '''
    if os.path.isfile('tags_genre_3000.csv'):

        # If csv file exists read in data from csv file.
        df = pd.read_csv('tags_genre_3000.csv', index_col=0)

    else:
        app_list = app_list
        tag_list = []
        genre_list = []

        for i in app_list:
            response = requests.get(f'https://steamspy.com/api.php?request=appdetails&appid={i}')
            response_data = response.json()
            if response_data['tags'] != []:
                tag_list.append(list(response_data['tags'].keys()))
                genre_list.append(response_data['genre'])
            else:
                tag_list.append([])
                genre_list.append(response_data['genre'])

        tag_series = pd.Series(tag_list, name='tags')
        genre_series = pd.Series(genre_list, name='genre')
        app_series = pd.Series(app_list, name='appid')

        df = pd.DataFrame(app_series)
        df['tags'] = tag_series
        df['genre'] = genre_series

        df.to_csv('tags_genre_3000.csv')

    return df

def get_appended_steamspy_data(steamspy_data, tags_genre):
    '''
    This function checks if device has required csv to run project.
    If not, requests data to create csv.
    '''
    if os.path.isfile('final_steamspy_3000_games.csv'):

        # If csv file exists read in data from csv file.
        df = pd.read_csv('final_steamspy_3000_games.csv', index_col=0)

    else:

        df = steamspy_data.reset_index()
        df = steamspy_data.drop(columns='index')

        df = pd.concat([steamspy_data,tags_genre], axis=1)

        df.to_csv('final_steamspy_3000_games.csv')

    return df

def get_clean_steamspy_data():
    '''
    This function runs all acquire and prep function.
    Ready for train,test splitting.
    '''
    if os.path.isfile('final_steamspy_3000_games.csv'):

        # If csv file exists read in data from csv file.
        df = pd.read_csv('final_steamspy_3000_games.csv', index_col=0)
        df = clean_steamspy(df)
    
    else:

        steamspy_data, app_list = get_steamspy_all()
        tags_genre = get_tags_genre(app_list)
        df = get_appended_steamspy_data(steamspy_data, tags_genre)

        df = clean_steamspy(df)

    return df
