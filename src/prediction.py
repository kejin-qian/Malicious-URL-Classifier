import pandas as pd
import numpy as np
import pickle as pkl
import logging
import argparse
import yaml
import os
import sys
import re
from os.path import splitext
import whois
import datetime
from urllib.parse import urlparse
import ipaddress as ip 
import iso3166
import tldextract
from sklearn import preprocessing

logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger('prediction')

def countdots(url): 
    """
    Count the number of dots appeared in URL.

    Args:
        url(string): url string
    Return:
        integer: number of dots counted.
    """  
    return url.count('.')

def containsip(url):
    """
    Check if an IP address present as the hostname in url.

    Args:
        url(string): url string
    Return:
        integer
        1 if an IP address appeared as the hostname
        0 if no IP address found
    """
    try:
        if ip.ip_address(url):
            return 1
    except:
        return 0

def CountSoftHyphen(url):
    """
    Count the number of soft hyphens appeared in url.

    Args:
        url(string): url string
    Return:
        integer: number of hyphens counted.
    """
    return url.count('-')

def CountAt(url):
    """
    Count the number of @ appeared in url.

    Args:
        url(string): url string
    Return:
        integer: number of @ counted.
    """
    return url.count('@')

def CountDSlash(url):
    """
    Count the number of double slashes appeared in url.

    Args:
        url(string): url string
    Return:
        integer: number of double slashes counted.
    """
    return url.count('//')

def countSubDir(url):
    """
    Count the number of subdirectories in url.

    Args:
        url(string): url string
    Return:
        integer: number of subdirectories counted.
    """
    return url.count('/')

def countSubDomain(subdomain):
    """
    Count the number of subdomains existed in url.

    Args:
        url(string): url string
    Return:
        integer: number of subdomains counted.
    """
    if not subdomain:
        return 0
    else:
        return len(subdomain.split('.'))

def countQueries(query):
    """
    Count the number of queries in url.

    Args:
        url(string): url string
    Return:
        integer: number of queries counted.
    """
    if not query:
        return 0
    else:
        return len(query.split('&'))

Suspicious_TLD=['zip','cricket','link','work','party','gq','kim','country','science','tk','download','xin','gdn',
                'racing','jetzt','stream','vip','bid','ren','load','mom','party','trade','date','wang','accountants',
               'bid','ltd','men','faith']

def get_ext(url):
    """
    Return the filename extension from url, or ''.
    
    Args:
        url(string): url string
    Return:
        ext(string): the file extension of the url
    """
    root, ext = splitext(url)
    return ext


def length(url):
    """
    Find the length of URL without https://www. or http://www. or http:// or https://

    Args:
        url(string): the url string
    Return:
        integer: lenth of the url
    """
    url = str(url)
    if url[:12] == 'https://www.':
        url = url[12:]
    elif url[:11] == 'http://www.':
        url = url[11:]
    elif url[:8] == 'https://':
        url = url[8:]
    elif url[:7] == 'http://':
        url = url[7:]
    else:
        url = url
    return np.log(len(url))

def url_format(url):
    """
    Change the format of url by adding http:// at the beginning if it doesn't have one.
    
    Args:
        url(string): url string
    Return:
        url(string): re-formatted url string
    """
    url = str(url)
    if url[:8] == 'https://' or url[:7] == 'http://':
        url = url
    else:
        url = 'http://' + url
    return url 

featureSet = pd.DataFrame(columns=('url','no of dots','no of hyphen','len of url','no of at',\
'no of double slash','no of subdir','no of subdomain','len of domain','no of queries','contains IP',
                                   'presence of Suspicious_TLD','create_age(months)','expiry_age(months)',
                                   'update_age(days)','country','file extension','label'))

def generateFeature(df):
    """
    Generate features for the url dataset and store them into the featureSet dataframe.

    Args:
        df(Pandas.DataFrame): DataFrame for all the urls
    
    Return:
        None
    """
    for i in range(20):
        try:
            # check whois API for domain documentation
            ext = tldextract.extract(df["url"].iloc[i])
            domain = '.'.join(ext[1:])
            w = whois.whois(domain)
            # if above works, generate all features
            features = getFeatures(df["url"].iloc[i], df["label"].iloc[i], w)
            featureSet.loc[i] = features
        except:
            features = getFeatures2(df["url"].iloc[i], df["label"].iloc[i])  
            featureSet.loc[i] = features

    logger.info('features have been generated for the url input.')

def getFeatures(url, w): 
    """
    Create features for each url string.

    Args:
        url(string): url string
        w: query result from Whois server. None if this url is not registered in Whois Server.

    Return:
        result(Pandas.DataFrame): dataframe used to store features generated
    """
    result = []
    url = str(url)
    
    #add the url to feature set
    result.append(url)
    
    #parse the URL and extract the domain information
    path = urlparse(url)
    ext = tldextract.extract(url)
    
    #counting number of dots in subdomain    
    result.append(countdots(ext.subdomain))
    
    #checking hyphen in domain   
    result.append(CountSoftHyphen(path.netloc))
    
    #length of URL    
    result.append(length(url))
    
    #checking @ in the url    
    result.append(CountAt(path.netloc))
    
    #checking presence of double slash    
    result.append(CountDSlash(path.path))
    
    #Count number of subdir    
    result.append(countSubDir(path.path))
    
    #number of sub domain    
    result.append(countSubDomain(ext.subdomain))
    
    #length of domain name    
    path2 = urlparse(url_format(url))
    result.append(len(path2.netloc))
    
    #count number of queries    
    result.append(len(path.query))
    
    #Adding domain information
    
    #if IP address is being used as a URL     
    result.append(containsip(ext.domain))
    
    #presence of Suspicious_TLD
    result.append(1 if ext.suffix in Suspicious_TLD else 0)
    
    #Get domain information by asking whois
    avg_month_time=365.2425/12.0
        
    #calculate creation age in months
                  
    if w.creation_date == None or type(w.creation_date) is str :
        result.append(-1)
        
    else:
        if(type(w.creation_date) is list): 
            create_date=w.creation_date[-1]
        else:
            create_date=w.creation_date

        if(type(create_date) is datetime.datetime):
            today_date=datetime.datetime.now()
            create_age_in_mon=((today_date - create_date).days)/avg_month_time
            create_age_in_mon=round(create_age_in_mon)
            result.append(create_age_in_mon)
            
        else:
            result.append(-1)
    
    #calculate expiry age in months
                  
    if(w.expiration_date==None or type(w.expiration_date) is str):
        result.append(-1)
    else:
        if(type(w.expiration_date) is list):
            expiry_date=w.expiration_date[-1]
        else:
            expiry_date=w.expiration_date
        if(type(expiry_date) is datetime.datetime):
            today_date=datetime.datetime.now()
            expiry_age_in_mon=((expiry_date - today_date).days)/avg_month_time
            expiry_age_in_mon=round(expiry_age_in_mon)

            # appending  in months Appended to the Vector
            result.append(expiry_age_in_mon)
        else:
            # expiry date error so append -1
            result.append(-1)

    #find the age of last update
                  
    if(w.updated_date==None or type(w.updated_date) is str):
        result.append(-1)
    else:
        if(type(w.updated_date) is list):
            update_date=w.updated_date[-1]
        else:
            update_date=w.updated_date
        if(type(update_date) is datetime.datetime):
            today_date=datetime.datetime.now()
            update_age_in_days=((today_date - update_date).days)
            result.append(update_age_in_days)
            # appending updated age in days Appended to the Vector
        else:
            result.append(-1)

    
    #find the country who is hosting this domain
    if(w.country == None):
        result.append("None")
    else:
        if isinstance(w.country,str):
            result.append(w['country'])
        else:
            result.append(w['country'][0])
    
    if get_ext(path.path) == '':
        result.append("None")
    else:
        result.append(get_ext(path.path))

    return result


#URLs without Whois information
def getFeatures2(url): 
    """
    Create features for each url string.

    url(string): url string

    Return:
        result(Pandas.DataFrame): dataframe used to store features generated
    """
    result = []
    url = str(url)
    
    #add the url to feature set
    result.append(url)
    
    #parse the URL and extract the domain information
    path = urlparse(url)
    ext = tldextract.extract(url)
    
    #counting number of dots in subdomain    
    result.append(countdots(ext.subdomain))
    
    #checking hyphen in domain   
    result.append(CountSoftHyphen(path.netloc))
    
    #length of URL    
    result.append(length(url))
    
    #checking @ in the url    
    result.append(CountAt(path.netloc))
    
    #checking presence of double slash    
    result.append(CountDSlash(path.path))
    
    #Count number of subdir    
    result.append(countSubDir(path.path))
    
    #number of sub domain    
    result.append(countSubDomain(ext.subdomain))
    
    #length of domain name    
    path2 = urlparse(url_format(url))
    result.append(len(path2.netloc)) 
    
    #count number of queries    
    result.append(len(path.query))
    
    #Adding domain information
    
    #if IP address is being used as a URL     
    result.append(containsip(ext.domain))
    
    #presence of Suspicious_TLD
    result.append(1 if ext.suffix in Suspicious_TLD else 0)
    
    #append default for create_age(months)country
    result.append(-1)
    
    #append default for expiry_age(months)
    result.append(-1)
    
    #append default for update_age(days)
    result.append(-1)
    
    #append default for country
    result.append('None')
    
    #append extension
    path = urlparse(url)
    
    if get_ext(path.path) == '':
        result.append('None')
    else:
        result.append(get_ext(path.path))
    
    
    return result


def readModel(model_path_in):
    """
    Read the trained Random Forest Classifier in.
    """
    with open(model_path_in, "rb") as f:
        RF = pkl.load(f)
    return RF


def generateFeature(url):
    """
    Generate features based on the provided usrl string.
    Args:
        url(string): url string provided
    """
    featureSet = pd.DataFrame(columns=('url','no of dots','no of hyphen','len of url','no of at',\
    'no of double slash','no of subdir','no of subdomain','len of domain','no of queries','contains IP',
                                   'presence of Suspicious_TLD','create_age(months)','expiry_age(months)',
                                   'update_age(days)','country','file extension'))

    try:
    # check whois API for domain documentation
        ext = tldextract.extract(url)
        domain = '.'.join(ext[1:])
        w = whois.whois(domain)
        # if above works, generate all features
        features = getFeatures(url, w)
        featureSet.loc[0] = features
        logger.info('{} has whois information'.format(url))
    except:
        features = getFeatures2(url)  
        featureSet.loc[0] = features
        logger.info('{} has no whois information, default value will be added.')

    features = featureSet.columns.tolist()
    features.remove('url')
    features.remove('country')
    features.remove('file extension')
    for f in features:
        featureSet[f] = featureSet[f].astype(int)
    # clean country code
    featureSet['file extension']=featureSet['file extension'].fillna('None')
    
    ## Create a new feature called Risk Indicator
    c1 = featureSet['no of dots'] >= 1
    c2 = featureSet['no of hyphen'] >= 1
    c3 = featureSet['no of subdir'] >= 6
    c4 = featureSet['contains IP'] == 1
    c5 = featureSet['presence of Suspicious_TLD'] == 1

    featureSet['risk indicator'] = np.array([c1 | c2| c3| c4| c5]).astype(int).T
    logger.info('risk indicator column has been created')

    country = featureSet.country
    new_country = []
    for i in range(len(country)):
        c = str(country[i])
        if c.upper() in iso3166.countries_by_name:
            new_country.append(iso3166.countries_by_name[c.upper()][1])
        elif len(c) == 2 and not c.isupper():
            new_country.append(c.upper())
        elif len(c) != 2 and c != 'REDACTED FOR PRIVACY':
            new_country.append('None')
        else:
            new_country.append(c)
    featureSet['country'] = new_country
    logger.debug('country column has been cleaned.')

    return featureSet


def getPrediction(model, featureSet, encoding_in, pred_out):
    """
    Transform and clean up the features generated.
    Make prediciton for the url based on the features generated.
    Save the prediciton result to a txt file.

    Args:
        model(pkl): saved Random Forest Classifier
        featureSet(Pandas.DataFrame): feature set generated based on the url string provided
        encoding_in(string): path to the saved one-hot encoding schema
        pred_out(string): path of where the prediction will be saved to

    Returns:
        tuple (predicted string result, predicted probability of being malicious, predicted 0/1 binary result)
    """

    # load the one-hot encoding schema used in training
    # one-hot encoding country and file extension 
    le = preprocessing.LabelEncoder()
    le.classes_ = np.load(encoding_in, allow_pickle=True) 
    featureSet['country'] = le.fit_transform(featureSet['country'])
    featureSet['file extension'] = le.fit_transform(featureSet['file extension'])
    logger.info('One-hot encoding has been done on country and file extension columns')
    
    # make class prediction
    y_pred_class = model.predict(featureSet.drop(['url', 'len of url', 'no of subdir'], axis = 1))
    # find the associated predicted probability
    y_pred_prob = model.predict_proba(featureSet.drop(['url', 'len of url', 'no of subdir'], axis = 1))

    y_pred_str = ''

    # use a classification threshold of 0.6
    if y_pred_prob[0][1] >= 0.6:
        y_pred_str = 'The url is malicious.'
        y_pred_binary = 1

    else:
        y_pred_str = 'The url is benign.'
        y_pred_binary = 0

    # write the prediction result to text file
    with open(pred_out,'w') as file:
        file.write(y_pred_str)

    logger.info('prediction result saved to the prediction folder.')
    return(y_pred_str, y_pred_prob[0][1], y_pred_binary)

def run_prediction(args):
    with open(args.config, 'r') as f:
        config = yaml.load(f)
    RF = readModel(**config['prediction']['readModel'])
    url = args.url
    featureSet = generateFeature(url)
    getPrediction(RF, featureSet, **config['prediction']['getPrediction'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make Predictions')
    parser.add_argument('--config', '-c', default = 'config.yml', help='path to yaml file with configurations')
    parser.add_argument('--url', help = 'url to be predicted')
    args = parser.parse_args()

    run_prediction(args)
