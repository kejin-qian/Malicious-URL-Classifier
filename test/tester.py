import pandas as pd
import sys
sys.path.append('../')
import os
import unittest

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


class MyTestCase(unittest.TestCase):

	def test_data_prep_importData(self):
		"""Test import data function from data_prep module.
		Check whether a pandas dataframe is formed and whether u
		the dataframe has the correct shape (31,3) (including one index column)"""

		
		self.assertTrue(isinstance(url_test, pd.DataFrame))
		
		self.assertEqual(url_test.shape,(31,2))

		with self.assertRaises(Exception) as context:
			dp.importData('test/data_not_exist.csv',0)
		self.assertTrue('File not found!' in str(context.exception))
		
	def test_data_prep_generate_finalize(self):
		"""Test generateFeature and finanlizeFeatures from data_prep module
		Check whether a pandas dataframe is formed and whether 
		the dataframe has the correct shape (31,20) (including one index column)"""
		
		self.assertTrue(isinstance(feature_test, pd.DataFrame))
		
		# line 13 when we read the csv created, column 0 is set to be index column
		# so the shape we would expect in this test would be (31, 19)
		expected_shape = (31, 20-1)
		self.assertEqual(feature_test.shape,(31,19))
		

	def test_encoding(self):
		"""Test onehotEncoding from encoding module
		Check whether the encoded feature set has the correct shape (31,16),
		including one index column"""
		
		# line 13 when we read the csv created, column 0 is set to be index column
		# so the shape we would expect in this test would be (31, 15)
		self.assertEqual(encoded_feature_test.shape,(31,15))


	def test_training_read(self):
		"""Test readData from the training module"""
		# shape expected to be (31,15) & (31,1)
		self.assertEqual(X.shape,(31,15))
		self.assertEqual(y.shape,(31,1))
		
		with self.assertRaises(Exception) as context:
			train.readData('test/not_exist1.csv', 'test/not_exist2.csv')
		self.assertTrue('File not found!' in str(context.exception))

	def test_training_save(self):
		"""Test trainModel and saveModel from training.py"""
		self.assertTrue(os.path.isfile('test/test_model.pkl'))

		
	def test_evaluation_read(self):
		"""Test whether the model is read in for evaluation correctly"""
		self.assertTrue(isinstance(RF_test, object))

		with self.assertRaises(Exception) as context:
			eva.readModel('test/model_exist.pkl')
		self.assertTrue('File not found!' in str(context.exception))
		
	def test_prediction(self):
		"""Test whether the the prediction module generate valid result"""
		result = None
		with open('test/test_pred.txt', 'r') as f:
			result = f.readlines()
		f.close()
		self.assertTrue(os.path.isfile('test/test_pred.txt'))
		# the result should only contain one line
		self.assertEqual(len(result),1)

		with self.assertRaises(Exception) as context:
			pred.getPrediction(RF_test, feature_test_url, 'test/test_classes_not_exist.npy', 'test/test_pred.txt')
		self.assertTrue('Encoding class not found!' in str(context.exception))

		
if __name__ == '__main__':
	unittest.mian()
	



