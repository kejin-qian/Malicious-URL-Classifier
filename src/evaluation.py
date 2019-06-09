import pandas as pd
import numpy as np
import seaborn as sns
import pickle as pkl
import logging
import argparse
import yaml
import prettytable
import matplotlib.pyplot as plt
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
logger = logging.getLogger('evaluation')

def readModel(model_path_in):
    """
    Read the trained model in.
    """
    with open(model_path_in, "rb") as f:
        RF = pkl.load(f)
    return RF

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
    return X, y

def splitData(X, y):
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
    X_train, X_test, y_train, y_test = train_test_split(X, y ,test_size=0.2, random_state = 1)
    return X_train, X_test, y_train, y_test 

def ModelEvaluation(model,x_test, y_test, out1, out2, out3, out4, out5, plot=True):
    """
    Evaluate the model performance and save confusion matrix, histogram of predicted probabilities, 
    model statistics along the way.

    Args:
        model: path to the Random Forest model trained
        x_test(Numpy.Array): test feature set
        y_test(Numpy.Array): test label set
        out1(string): path to save the confusion matrix as a csv file
        out2(string): path to save the heapmap visualization of the confusion matrix
        out3(string): path to save the histogram of predicted probabilities
        out4(string): path to save the visualization of the ROC curve
        out5(string): path to save all the model evaluation stats in a txt file
        plot(bool, default True): True to save plots as jpg files, False otherwise
    """
    y_pred_class = model.predict(x_test)
    # calculate accuracy
    accuracy = metrics.accuracy_score(y_test, y_pred_class)
    
    # test set class balance
    bad_percent = y_test.mean()
    
    #Confusion matrix
    confusion = metrics.confusion_matrix(y_test, y_pred_class)
    cfm = pd.DataFrame(data=confusion) 
    # save confusion matrix
    cfm.to_csv(out1)
    
    # visualize Confusion Matrix
    plt.figure(1)
    sns.heatmap(confusion,annot=True,fmt="d") 
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    # save confusion matrix heatmap
    plt.savefig(out2)
    
    # False Positive Rate
    FP = (confusion[0][1] / float(sum(confusion[0])))
    FN = (confusion[1][0] / float(sum(confusion[1])))
    F1 = f1_score(y_test, y_pred_class, average='binary')
    logger.debug('F1 score is {}'.format(F1))

    # Precision
    Precision = metrics.precision_score(y_test, y_pred_class)
    auc = metrics.roc_auc_score(y_test, y_pred_class)

    
    # store the predicted probabilities for class 1
    y_pred_prob = model.predict_proba(x_test)[:, 1]
    
    logger.debug('plot option is set to be {}'.format(plot))
    if plot == True:
        # histogram of predicted probabilities
        # adjust the font size 
        plt.figure(2)
        plt.rcParams['font.size'] = 12
        # 8 bins
        plt.hist(y_pred_prob, bins=8, color="mediumpurple")
        
        # x-axis limit from 0 to 1
        plt.xlim(0,1)
        plt.title('Histogram of predicted probabilities')
        plt.xlabel('Predicted probability of being malicious')
        plt.ylabel('Frequency')
        # save prediction probability histogram
        plt.savefig(out3)

    roc_auc = metrics.roc_auc_score(y_test, y_pred_prob)
    
    fpr, tpr, thresholds = metrics.roc_curve(y_test, y_pred_prob)
    if plot == True:
        plt.figure(3)
        plt.plot(fpr, tpr, color="mediumpurple", label='ROC curve (area = %0.2f)' % roc_auc)
        plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.0])
        plt.rcParams['font.size'] = 12
        plt.title('ROC curve for malicious url classifier')
        plt.xlabel('False Positive Rate (1 - Specificity)')
        plt.ylabel('True Positive Rate (Sensitivity)')
        plt.legend(loc="lower right")
        # save ROC
        plt.savefig(out4)
    
    model_eval = prettytable.PrettyTable(["Random Forest", "n_estimators = 150"])
    model_eval.add_row(["Classification Accuracy", accuracy])
    model_eval.add_row(["False Positive", FP]) 
    model_eval.add_row(["False Negative", FN]) 
    model_eval.add_row(["F1 Score", F1])  
    model_eval.add_row(["AUC", roc_auc])
    table_txt = model_eval.get_string()
    with open(out5,'w') as file:
        file.write(table_txt)

def featureRank(RF, X, features_in, rank_txt_out):
    """
    Get the feature importance from the random forest model and save them into a txt file

    Args:
        RF: Random Forest model
        X(Numpy.nd-array): feature data
        features_in(Pandas.DataFrame): path to feature dataset
        rank_txt_out(string): path to a txt file where feature importance will be written to
    """

    # load dataset
    featureSet = pd.read_csv(features_in, index_col = 0)
    # load model
    forest = RF
    # get the feature importance from the trained model
    importances = forest.feature_importances_
    logger.info('feautre importances were retrieved from the random forest model')
    logger.debug('feature importances data has length {}'.format(importances.size))

    std = np.std([tree.feature_importances_ for tree in forest.estimators_],
                 axis=0)
    indices = np.argsort(importances)[::-1]
    # write feature rank into a text file
    for f in range(X.shape[1]):
        with open(rank_txt_out, 'a') as k:
            k.write("%d. feature %s (%f) \n" % (f + 1, list(featureSet)[indices[f]], importances[indices[f]]))
        k.close()

def run_evaluation(args):
    with open(args.config, 'r') as f:
        config = yaml.load(f)
    RF = readModel(**config['evaluation']['readModel'])
    X, y = readData(**config['evaluation']['readData'])
    X_train, X_test, y_train, y_test = splitData(X, y)
    ModelEvaluation(RF, X_test, y_test, plot=True, **config['evaluation']['ModelEvaluation'])
    featureRank(RF, X, **config['evaluation']['featureRank'] )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Model Evaluation')
    parser.add_argument('--config', '-c', default = 'config.yml', help='path to yaml file with configurations')
    args = parser.parse_args()

    run_evaluation(args)

