import pandas as pd
import sys
sys.path.append('../')
import os

import src.data_prep as dp
import src.encoding as ec
import src.training as train
import src.evaluation as eva
import src.prediction as pred


# dataset for testing
url_test = dp.importData('test/test_url.csv', 0)
# not sure if it will work
dp.generateFeature(url_test, 31)
dp.finalizeFeatures(dp.featureSet, 'test/test_finalize_feature_result.csv')
feature_test = pd.read_csv('test/test_finalize_feature_result.csv', index_col = 0)

# encoding
ec.onehotEncoding(feature_test, 'test/test_classes.npy', 'test/test_ModelfeatureSet.csv', 'test/test_modelLabel.csv')
encoded_feature_test =  pd.read_csv('test/test_ModelfeatureSet.csv', index_col = 0)

# training
X, y = train.readData('test/test_ModelfeatureSet.csv', 'test/test_modelLabel.csv')
X_train, X_test, y_train, y_test = train.splitData(X,y,0.2,1)

train.saveModel(X_train, y_train, "test/test_model.pkl")

# evaluation
RF_test = eva.readModel("test/RandomForest.pkl")

# training
url = "http://www.expedia.com"
feature_test_url = pred.generateFeature(url)
pred.getPrediction(RF_test, feature_test_url, 'test/test_classes.npy', 'test/test_pred.txt')


def test_data_prep_importData():
	"""Test import data function from data_prep module.
	Check whether a pandas dataframe is formed and whether u
	the dataframe has the correct shape (31,3) (including one index column)"""

	
	assert isinstance(url_test, pd.DataFrame)
	
	assert url_test.shape == (31,2)
	
	
def test_data_prep_generate_finalize():
	"""Test generateFeature and finanlizeFeatures from data_prep module
	Check whether a pandas dataframe is formed and whether 
	the dataframe has the correct shape (31,20) (including one index column)"""
	
	assert isinstance(feature_test, pd.DataFrame)
	
	# line 13 when we read the csv created, column 0 is set to be index column
	# so the shape we would expect in this test would be (31, 19)
	expected_shape = (31, 20-1)
	assert feature_test.shape == (31,19)
	

def test_encoding():
	"""Test onehotEncoding from encoding module
	Check whether the encoded feature set has the correct shape (31,16),
	including one index column"""
	
	# line 13 when we read the csv created, column 0 is set to be index column
	# so the shape we would expect in this test would be (31, 15)
	assert encoded_feature_test.shape == (31,15)

def test_training_read():
	"""Test readData from the training module"""
	# shape expected to be (31,15) & (31,1)
	assert X.shape == (31,15)
	assert y.shape == (31,1)
	

def test_training_save():
	"""Test trainModel and saveModel from training.py"""
	assert os.path.isfile('test/test_model.pkl') == True
	
def test_evaluation_read():
	"""Test whether the model is read in for evaluation correctly"""
	assert isinstance(RF_test, object)
	
def test_prediction():
	"""Test whether the the prediction module generate valid result"""
	result = None
	with open('test/test_pred.txt', 'r') as f:
		result = f.readlines()
	f.close()
	assert os.path.isfile('test/test_pred.txt') == True
	# the result should only contain one line
	assert len(result) == 1

	
	
	



