import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

import pandas as pd
import matplotlib.pyplot as plt
# Machine Learning libraries
# model selection
from sklearn.model_selection import GridSearchCV
# classifiers
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
import xgboost as xgb
# helper preprocessing module

from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

def prep_for_model(train, validate,test):
    #df = df.drop(columns = ['binned_hours_explore','binned_release_price','median_2weeks','appid','name','developer','publisher','positive','negative','owners','average_forever','average_2weeks','median_forever','price','initialprice','discount','ccu','appid.1','tags','genre','Publisher_','Developer_','Genre_nan'])
    train = train.drop(columns = ['binned_hours_explore','binned_release_price','median_2weeks','appid','name','developer','publisher','positive','negative','owners','average_forever','average_2weeks','median_forever','price','initialprice','discount','ccu','appid.1','tags','genre','Publisher_','Developer_','Genre_nan'])
    validate = validate.drop(columns = ['binned_hours_explore','binned_release_price','median_2weeks','appid','name','developer','publisher','positive','negative','owners','average_forever','average_2weeks','median_forever','price','initialprice','discount','ccu','appid.1','tags','genre','Publisher_','Developer_','Genre_nan'])
    test = test.drop(columns = ['binned_hours_explore','binned_release_price','median_2weeks','appid','name','developer','publisher','positive','negative','owners','average_forever','average_2weeks','median_forever','price','initialprice','discount','ccu','appid.1','tags','genre','Publisher_','Developer_','Genre_nan'])
    return train, validate, test
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
    x_train = pd.DataFrame(scaler.transform(x_train), columns = x_train.columns)
    x_validate = pd.DataFrame(scaler.transform(x_validate), columns = x_validate.columns)
    x_test = pd.DataFrame(scaler.transform(x_test), columns = x_test.columns)
    return x_train, x_validate, x_test

def initialize_models():
    '''
    This function initializes a dataframe, and lists for scoring
    the models used for the project.
    '''
    depth_list = []
    sample_list = []
    c_val_list = []
    for x in range(1,21,1):
        depth_list.append(x)
    for x in range(1,21,1):
        sample_list.append(x)
    for x in range(5,100,5):
        c_val_list.append(x/100)

    scores = pd.DataFrame(columns=['model_name', 'train_score', 'validate_score', 'score_difference'])
    
    return scores, depth_list, c_val_list

def get_decision_tree_results(x_train, y_train, x_validate, y_validate, depth_list, scores):
    '''
    This function
    '''
    
    DTC_parameters = {'max_depth':depth_list}
    
    DTC = DecisionTreeClassifier(random_state=142)
    
    cv = 5
    
    grid_DTC = GridSearchCV(estimator=DTC, param_grid=DTC_parameters, cv=cv, n_jobs=-1)
    
    grid_DTC.fit(x_train, y_train)
    train_score = grid_DTC.best_estimator_.score(x_train, y_train)
    validate_score = grid_DTC.best_estimator_.score(x_validate, y_validate)
    
    print(f'Best parameters per algorithm:')
    print('----------------------------------------------------')
    print(f'Decision Tree Parameters:  {grid_DTC.best_params_}')
    
    scores.loc[len(scores)] = ['Decision Tree', train_score, validate_score, train_score - validate_score]
    
    y_preds_train = pd.DataFrame({
        'y_act': y_train,
        'baseline': 92,
        'DTC': grid_DTC.predict(x_train)})
    y_preds_validate = pd.DataFrame({
        'y_act': y_validate,
        'baseline': 92,
        'DTC': grid_DTC.predict(x_validate)})
    print(pd.DataFrame(classification_report(y_preds_validate.y_act, y_preds_validate.DTC, output_dict=True)))

    return scores


def get_random_forest_results(x_train, y_train, x_validate, y_validate, depth_list, scores):
    
    RF_parameters = {'max_depth':depth_list}
    
    RF = RandomForestClassifier(random_state=142)
    
    cv = 5
    
    grid_RF = GridSearchCV(estimator=RF, param_grid=RF_parameters, cv=cv, n_jobs=-1)
    
    grid_RF.fit(x_train, y_train)
    train_score = grid_RF.best_estimator_.score(x_train, y_train)
    validate_score = grid_RF.best_estimator_.score(x_validate, y_validate)
    
    print(f'Best parameters per algorithm:')
    print('----------------------------------------------------')
    print(f'Random Forest Parameters:  {grid_RF.best_params_}')
    
    scores.loc[len(scores)] = ['Random Forest', train_score, validate_score, train_score - validate_score]
    
    y_preds_train = pd.DataFrame({
        'y_act': y_train,
        'baseline': 92,
        'RF': grid_RF.predict(x_train)})
    y_preds_validate = pd.DataFrame({
        'y_act': y_validate,
        'baseline': 92,
        'RF': grid_RF.predict(x_validate)})
    print(pd.DataFrame(classification_report(y_preds_validate.y_act, y_preds_validate.RF, output_dict=True)))


    return scores

def get_knn_results(x_train, y_train, x_validate, y_validate, scores):
    
    KNN_parameters = {'n_neighbors':[1,2,3,4,5]}
    
    KNN = KNeighborsClassifier(n_neighbors=5, weights='uniform')
    
    cv = 5
    
    grid_KNN = GridSearchCV(estimator=KNN, param_grid=KNN_parameters, cv=cv, n_jobs=-1)
    
    grid_KNN.fit(x_train, y_train)
    train_score = grid_KNN.best_estimator_.score(x_train, y_train)
    validate_score = grid_KNN.best_estimator_.score(x_validate, y_validate)
    
    print(f'Best parameters per algorithm:')
    print('----------------------------------------------------')
    print(f'KNN Parameters:  {grid_KNN.best_params_}')
    
    scores.loc[len(scores)] = ['KNN', train_score, validate_score, train_score - validate_score]
    
    y_preds_train = pd.DataFrame({
        'y_act': y_train,
        'baseline': 92,
        'KNN': grid_KNN.predict(x_train)})
    y_preds_validate = pd.DataFrame({
        'y_act': y_validate,
        'baseline': 92,
        'KNN': grid_KNN.predict(x_validate)})
    print(pd.DataFrame(classification_report(y_preds_validate.y_act, y_preds_validate.KNN, output_dict=True)))


    return scores

def get_log_reg_results(x_train, y_train, x_validate, y_validate, c_val_list, scores):
    
    LR_parameters = {'C':c_val_list}
    
    LR = LogisticRegression(solver='liblinear')
    
    cv = 5
    
    grid_LR = GridSearchCV(estimator=LR, param_grid=LR_parameters, cv=cv, n_jobs=-1)
    
    grid_LR.fit(x_train, y_train)
    train_score = grid_LR.best_estimator_.score(x_train, y_train)
    validate_score = grid_LR.best_estimator_.score(x_validate, y_validate)
    
    print(f'Best parameters per algorithm:')
    print('----------------------------------------------------')
    print(f'LR Parameters:  {grid_LR.best_params_}')
    
    scores.loc[len(scores)] = ['LR', train_score, validate_score, train_score - validate_score]
    
    y_preds_train = pd.DataFrame({
        'y_act': y_train,
        'baseline': 92,
        'LR': grid_LR.predict(x_train)})
    y_preds_validate = pd.DataFrame({
        'y_act': y_validate,
        'baseline': 92,
        'LR': grid_LR.predict(x_validate)})
    print(pd.DataFrame(classification_report(y_preds_validate.y_act, y_preds_validate.LR, output_dict=True)))



    return scores

def get_knn_test(x_train, y_train, x_test, y_test):
    
    
    scores = pd.DataFrame(columns=['model_name', 'train_score', 'test_score', 'score_difference'])
    
    KNN_parameters = {'n_neighbors':[1,2,3,4,5]}
    
    KNN = KNeighborsClassifier(n_neighbors=5, weights='uniform')
    
    cv = 5
    
    grid_KNN = GridSearchCV(estimator=KNN, param_grid=KNN_parameters, cv=cv, n_jobs=-1)
    
    grid_KNN.fit(x_train, y_train)
    train_score = grid_KNN.best_estimator_.score(x_train, y_train)
    test_score = grid_KNN.best_estimator_.score(x_test, y_test)
    
    print(f'Best parameters per algorithm:')
    print('----------------------------------------------------')
    print(f'KNN Parameters:  {grid_KNN.best_params_}')

    scores.loc[len(scores)] = ['KNN', train_score, test_score, train_score - test_score]

    y_preds_train = pd.DataFrame({
        'y_act': y_train,
        'baseline': 92,
        'KNN': grid_KNN.predict(x_train)})
    y_preds_test = pd.DataFrame({
        'y_act': y_test,
        'baseline': 92,
        'KNN': grid_KNN.predict(x_test)})
    print(pd.DataFrame(classification_report(y_preds_test.y_act, y_preds_test.KNN, output_dict=True)))
    
    return scores
