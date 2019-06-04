
import pandas as pd
import numpy as np
import pickle as pkl
import logging
import argparse
import yaml
#import machine learning package
import sklearn.ensemble as ek
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_validate
from sklearn.model_selection import cross_val_score
from sklearn import tree, linear_model
from sklearn import metrics
from sklearn.feature_selection import SelectFromModel
from sklearn.externals import joblib
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import binarize, LabelEncoder, MinMaxScaler
from sklearn import svm
from sklearn.metrics import f1_score
from sklearn.linear_model import LogisticRegression
from sklearn import preprocessing

logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger()

def readData(feature_in, label_in):
    X = pd.read_csv(feature_in, index_col = 0).values
    y = pd.read_csv(label_in, header = None, index_col = 0).values
    return X, y

def splitData(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y ,test_size=0.2, random_state = 1)
    return X_train, X_test, y_train, y_test 

def trainModel(X,y):
    np.random.seed(123)
    RandomForest = ek.RandomForestClassifier(n_estimators=150, random_state = 1)
    cv_results = cross_validate(RandomForest, X, y, cv=10,return_train_score=True) 
    logger.info('10-fold cross validation accuracy of the model is: {}'.format(cv_results['test_score'].mean()))

def saveModel(X_train, y_train, model_out):
    RandomForest = ek.RandomForestClassifier(n_estimators=150, random_state = 1)
    RandomForest.fit(X_train,y_train.ravel())
    with open(model_out, 'wb') as f:
        pkl.dump(RandomForest, f)
    logger.info('Model is saved to {}'.format(model_out))

def run_training(args):
    with open(args.config, 'r') as f:
        config = yaml.load(f)

    X, y = readData(**config['training']['readData'])
    X_train, X_test, y_train, y_test = splitData(X,y)
    trainModel(X,y)
    saveModel(X_train, y_train,**config['training']['saveModel'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train model')
    parser.add_argument('--config', '-c', default = 'config.yml', help='path to yaml file with configurations')
    args = parser.parse_args()

    run_training(args)

