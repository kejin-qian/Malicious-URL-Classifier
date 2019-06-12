#import packages
import pandas as pd
import numpy as np
#import machine learning package
from sklearn import preprocessing
from sklearn.preprocessing import binarize, LabelEncoder, MinMaxScaler
import logging
import argparse
import yaml

logging.basicConfig(filename='url_classifier.log', filemode='a', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger('encoding')

def readData(saved_filepath_in):
    """import complete feature set generated from data_prep.py"""

    URLdata = pd.read_csv(saved_filepath_in, index_col = 0)
    logger.info('Feature data successfully loaded in.')
    return URLdata

def onehotEncoding(URLdata, encoding_out, feature_out, label_out):
    """
    Apply one-hot encoding to country and file extension
    
    Args:
        URLdata(Pandas.DataFrame): Feature data read from readData
        encoding_out(string): path to save the encoding schema classes.npy file
        feature_out(string): path to save the feature-only dataset (label removed)
        label_out(string): path to save the label-only dataset
    """
    le = preprocessing.LabelEncoder()
    URLdata['country'] = le.fit_transform(URLdata['country'])
    URLdata['file extension'] = le.fit_transform(URLdata['file extension'])
    logger.info('country column has type {}'.format(type(URLdata['country'])))
    logger.info('One-hot encoding has been applied to country and file extension columns.')
    np.save(encoding_out, le.classes_)
    logger.info('One-hot encoding schema saved to the model folder.')
    
    ## Extract the Feature Set and Response Column
    ## Save them for future use
    X = URLdata.drop(['url','label', 'len of url', 'no of subdir'],axis=1)
    X.to_csv(feature_out)
    X = URLdata.drop(['url','label'],axis=1).values
    y = URLdata['label']
    y.to_csv(label_out)
    y = URLdata['label'].values

def run_encoding(args):
    with open(args.config, 'r') as f:
        config = yaml.load(f)

    URLdata = readData(**config['encoding']['readData'])
    onehotEncoding(URLdata,**config['encoding']['onehotEncoding'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='One-hot encoding')
    parser.add_argument('--config', '-c', default = 'config.yml', help='path to yaml file with configurations')
    args = parser.parse_args()

    run_encoding(args)

