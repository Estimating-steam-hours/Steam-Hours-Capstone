import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()

#Creating list of top publishers
AAA = ['Tencent Games','Sony Interactive','Microsoft','Activision Blizzard','Electronic Arts','Nintendo','Bandai Namco','Take-Two Interactive','Ubisoft','Square Enix']

def clean_steamspy(df):
#GENRE ENCODING:
### FINDS UNIQUE WORDS FROM LIST OF GENRES
    '''genre_list = ['']
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
        df[f'Genre_{x}'] = df.genres.str.contains(x)'''
#Turning minutes to hours
    df.iloc[:,[9,10,11,12]] = (df.iloc[:,[9,10,11,12]] / 120)
#Drops
    df = df.drop(columns = ['score_rank','userscore','owners'])
    return df

def scale_numeric(df):
    df.iloc[:,[6,7,8,9,10]] = scaler.fit_transform(df.iloc[:,[6,7,8,9,10]])
    return df
def my_train_test_split(df, target):

    train, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train, test_size=.25, random_state=123)

    return train, validate, test
