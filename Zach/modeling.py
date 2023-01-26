import pandas as pd
import numpy as np
def prep_for_model(df):
    df = df.drop(columns = ['median_2weeks','appid','name','developer','publisher','positive','negative','owners','average_forever','average_2weeks','median_forever','price','initialprice','discount','ccu','appid.1','tags','genre','Publisher_','Developer_','Publisher__Inc.','Developer__Inc.','Genre_nan'])
    return df