import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
import numpy as np

#Creating list of top 10 publishers from https://learn.g2.com/video-game-publishers

AAA = ['Tencent Games','Sony Interactive','Microsoft','Activision Blizzard','Electronic Arts','Nintendo','Bandai Namco','Take-Two Interactive','Ubisoft','Square Enix']

#Creating a list of top 10 indie publishers from https://ninichimusic.com/blog/16-indie-friendly-indie-game-publishers

III = ['Curve Digital','Ukuza','Team 17','Devolver Digital','Indie Fund','Midnight City','Serenity Forge','Noodlecake Studios','Versus Evil','Mode 7 Games']


def clean_steamspy(df):
    #Turning minutes to hours
    df.iloc[:,[9,10,11,12]] = (df.iloc[:,[9,10,11,12]] / 60)
    #BINS FOR TARGET
    ninety = np.quantile(df['average_forever'], 0.90)
    ten = np.quantile(df['average_forever'], 0.10)
    IQR = ninety - ten
    target_bins = [0,1.565,75.253,195.97,1000]
    target_labels = ['rarely_played','moderately_played','heavily_played','most_played']
    df['binned_hours'] = pd.cut(df['average_forever'], bins = target_bins, labels = target_labels)

    #BINS FOR RELEASE PRICE
    price_bins = [0,200,400,10000]
    price_labels = ['free_to_play','budget_games','full_price_games']
    df['binned_release_price'] = pd.cut(df['initialprice'], bins = price_bins, labels = price_labels)


    #formatting pub and dev strings
    df.publisher = df.publisher.str.replace(' ', '_')
    df.developer = df.developer.str.replace(' ','_')
    df = df[df.average_forever > 0]
#PUBLISHER ENCODING:
    Publisher_list = ['']
    word = ''
    for x in df.publisher[(df.binned_hours == 'most_played') & (df.owners != '0 .. 20,000') & (df.owners != '20,000 .. 50,000') & (df.owners != '50,000 .. 100,000') & (df.owners != '100,000 .. 200,000') & (df.owners != '200,000 .. 500,000') & (df.owners != '500,000 .. 1,000,000')].tolist():
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
    for x in df.developer[(df.binned_hours == 'most_played') & (df.owners != '0 .. 20,000') & (df.owners != '20,000 .. 50,000') & (df.owners != '50,000 .. 100,000') & (df.owners != '100,000 .. 200,000') & (df.owners != '200,000 .. 500,000') & (df.owners != '500,000 .. 1,000,000')].tolist():
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

#Drops
    df = df.drop(columns = ['score_rank','userscore'])
    df = df.dropna()
    return df

def scale_numeric(df):
    df.iloc[:,[6,7,8,9,10]] = scaler.fit_transform(df.iloc[:,[6,7,8,9,10]])
    return df
def my_train_test_split(df):

    train, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train, test_size=.25, random_state=123)

    return train, validate, test
