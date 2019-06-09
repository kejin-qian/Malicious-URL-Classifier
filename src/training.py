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

logging.basicConfig(filename='url_classifier.log', filemode='a', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger('training')

def readData(feature_in, label_in):
    """
    Read in the feature set and label set as dataframe.

    Args:
        feature_in(string): the local path to the ModelfeatureSet.csv
        label_in(string): the local path to the ModelLabel.csv
    Return:
        X(numpy.ndarray): final feature set
        y(numpy.ndarray): final label set
    """
    X = pd.read_csv(feature_in, index_col = 0).values
    y = pd.read_csv(label_in, header = None, index_col = 0).values
    logger.info('Feature and Label sets have been loaded in.')
    return X, y

def splitData(X, y, test_size, random_state):
    """
    Split arrays into random train and test subsets.

    Args:
        X(numpy.ndarray): Feature Set 
        y(numpy.ndarray): Label Set

    Return:
        X_train: training feature set
        X_test: test feature set
        y_train: training label set
        y_test: test label set
    """
    X_train, X_test, y_train, y_test = train_test_split(X, y ,test_size=test_size, random_state = random_state)
    logger.debug('Size of the training set is {}'.format(X_train.size))
    return X_train, X_test, y_train, y_test 

def trainModel(X,y):
    """
    Fit a predictive classification model using Random Forest Classifier.
    Show 10-fold cross validation result.

    Args:
        X(numpy.ndarray): Feature Set
        y(numpy.ndarray): Label Set
    """
    np.random.seed(123)
    RandomForest = ek.RandomForestClassifier(n_estimators=150, random_state = 1)
    cv_results = cross_validate(RandomForest, X, y, cv=10,return_train_score=True) 
    logger.info('10-fold cross validation accuracy of the model is: {}'.format(cv_results['test_score'].mean()))

def saveModel(X_train, y_train, model_out):
    """
    Train the model on training sets and save the model pkl file for future use.
    """
    RandomForest = ek.RandomForestClassifier(n_estimators=150, random_state = 1)
    RandomForest.fit(X_train,y_train.ravel())
    with open(model_out, 'wb') as f:
        pkl.dump(RandomForest, f)
    logger.info('Model is saved to {}'.format(model_out))

def run_training(args):
    with open(args.config, 'r') as f:
        config = yaml.load(f)

    X, y = readData(**config['training']['readData'])
    X_train, X_test, y_train, y_test = splitData(X,y, **config['training']['splitData'])
    trainModel(X,y)
    saveModel(X_train, y_train,**config['training']['saveModel'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train model')
    parser.add_argument('--config', '-c', default = 'config.yml', help='path to yaml file with configurations')
    args = parser.parse_args()

    run_training(args)

