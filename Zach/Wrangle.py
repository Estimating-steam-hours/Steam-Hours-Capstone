import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

def clean_steamspy(df):
#PUBLISHER ENCODING:
    Publisher_list = ['']
    word = ''
    for x in df.publisher.tolist():
        for a in str(x):
            if a != '|':
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
        Publisher_list.remove(x)
        x = x.replace(' ','_')
        Publisher_list.append(x)
    Publisher_list.remove('')
    for x in Publisher_list:
        df[f'Publisher_{x}'] = df.publisher.str.contains(x)
#Developer ENCODING:
    Developer_list = ['']
    word = ''
    for x in df.developer.tolist():
        for a in str(x):
            if a != '|':
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
        Developer_list.remove(x)
        x = x.replace(' ','_')
        Developer_list.append(x)
    Developer_list.remove('')
    for x in Developer_list:
        df[f'Developer_{x}'] = df.developer.str.contains(x)
#Genre encoding
#GENRE ENCODING:
### FINDS UNIQUE WORDS FROM LIST OF GENRES
    genre_list = ['']
    word = ''
    for x in df.genres.tolist():
        for a in str(x):
            if a != '|':
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
    genre_list.remove('')
    for x in genre_list:
        genre_list.remove(x)
        x = x.replace(' ','_')
        genre_list.append(x)
    for x in genre_list:
        df[f'Genre_{x}'] = df.genres.str.contains(x)
#Turning minutes to hours
    df.iloc[:,[9,10,11,12]] = (df.iloc[:,[9,10,11,12]] / 120)
#Drops
    df = df.drop(columns = ['score_rank','userscore','price','initialprice','discount','owners'])
    return df
#Tags encoding
    tags_list = ['']
    word = ''
    for x in df.tags.tolist():
        for a in str(x):
            if a != '|':
                word = word + a
            else:
                if word not in tags_list:
                    tags_list.append(word)
                    word = ''
                word = ''
        if word not in tags_list:
            tags_list.append(word)
            word = ''
        word = ''
    for x in tags_list:
        tags_list.remove(x)
        x = x.replace(' ','_')
        tags_list.append(x)
    tags_list.remove('')
    for x in tags_list:
        df[f'Tag_{x}'] = df.developer.str.contains(x)

def scale_numeric(df):
    df.iloc[:,[6,7,8,9,10]] = scaler.fit_transform(df.iloc[:,[6,7,8,9,10]])
    return df
def my_train_test_split(df, target):

    train, test = train_test_split(df, test_size=.2, random_state=123, stratify=df[target])
    train, validate = train_test_split(train, test_size=.25, random_state=123, stratify=train[target])

    return train, validate, test
