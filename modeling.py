import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

def prep_for_model(df,train, validate,test):
    df = df.drop(columns = ['binned_hours_explore','binned_release_price','median_2weeks','appid','name','developer','publisher','positive','negative','owners','average_forever','average_2weeks','median_forever','price','initialprice','discount','ccu','appid.1','tags','genre','Publisher_','Developer_','Genre_nan'])
    train = train.drop(columns = ['binned_hours_explore','binned_release_price','median_2weeks','appid','name','developer','publisher','positive','negative','owners','average_forever','average_2weeks','median_forever','price','initialprice','discount','ccu','appid.1','tags','genre','Publisher_','Developer_','Genre_nan'])
    validate = validate.drop(columns = ['binned_hours_explore','binned_release_price','median_2weeks','appid','name','developer','publisher','positive','negative','owners','average_forever','average_2weeks','median_forever','price','initialprice','discount','ccu','appid.1','tags','genre','Publisher_','Developer_','Genre_nan'])
    test = test.drop(columns = ['binned_hours_explore','binned_release_price','median_2weeks','appid','name','developer','publisher','positive','negative','owners','average_forever','average_2weeks','median_forever','price','initialprice','discount','ccu','appid.1','tags','genre','Publisher_','Developer_','Genre_nan'])
    return df, train, validate, test
def isolate_target(train,validate,test):
    x_train = train.drop(columns = 'binned_hours')
    y_train = train.binned_hours
    x_validate = validate.drop(columns = 'binned_hours')
    y_validate = validate.binned_hours
    x_test = test.drop(columns = 'binned_hours')
    y_test = test.binned_hours

    return x_train, y_train, x_validate, y_validate, x_test, y_test
def scale_data(x_train,x_validate,x_test):
    scaler = MinMaxScaler()
    scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    x_validate = scaler.transform(x_validate)
    x_test = scaler.transform(x_test)
    return x_train, x_validate, x_test