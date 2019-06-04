#import packages
import pandas as pd
import numpy as np
#import machine learning package
from sklearn.preprocessing import binarize, LabelEncoder, MinMaxScaler
from sklearn import preprocessing
import logging
import argparse
import yaml

logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger()

def readData(saved_filepath_in):
    # import complete feature set made from Data Cleaning and EDA notebook
    URLdata = pd.read_csv(saved_filepath_in, index_col = 0)
    return URLdata

def onehotEncoding(URLdata, encoding_out, feature_out, label_out):
    # Apply one-hot encoding to country and file extension
    le = preprocessing.LabelEncoder()
    URLdata['country'] = le.fit_transform(URLdata['country'])
    URLdata['file extension'] = le.fit_transform(URLdata['file extension'])
    np.save(encoding_out, le.classes_)
    
    ## Extract the Feature Set and Response Column
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

