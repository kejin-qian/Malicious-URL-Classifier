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


def countdots(url):  
    return url.count('.')

def containsip(url):
    try:
        if ip.ip_address(url):
            return 1
    except:
        return 0

def CountSoftHyphen(url):
    return url.count('-')

def CountAt(url):
    return url.count('@')

def CountDSlash(url):
    return url.count('//')

def countSubDir(url):
    return url.count('/')

def countSubDomain(subdomain):
    if not subdomain:
        return 0
    else:
        return len(subdomain.split('.'))

def countQueries(query):
    if not query:
        return 0
    else:
        return len(query.split('&'))

Suspicious_TLD=['zip','cricket','link','work','party','gq','kim','country','science','tk','download','xin','gdn',
                'racing','jetzt','stream','vip','bid','ren','load','mom','party','trade','date','wang','accountants',
               'bid','ltd','men','faith']
#trend micro's top 10 malicious domains 
Suspicious_Domain=['luckytime.co.kr','mattfoll.eu.interia.pl','trafficholder.com','dl.baixaki.com.br',
                   'bembed.redtube.comr','tags.expo9.exponential.com','deepspacer.com','funad.co.kr',
                   'trafficconverter.biz', 'alegroup.info']

def get_ext(url):
    """Return the filename extension from url, or ''."""
    root, ext = splitext(url)
    return ext


def length(url):
    """
    Find the length of URL without https://www. or http://www. or http:// or https://
    
    Used to correct the calculation of the length of each URL
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

def getFeatures(url, w): 
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
    with open(model_path_in, "rb") as f:
        RF = pkl.load(f)
    return RF


def generateFeature(url):
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
    except:
        features = getFeatures2(url)  
        featureSet.loc[0] = features

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
    return featureSet


def getPrediction(model, featureSet, encoding_in, pred_out):
    """slightly modify features then save features generated to a csv file
    """

    le = preprocessing.LabelEncoder()
    le.classes_ = np.load(encoding_in, allow_pickle=True) 
    featureSet['country'] = le.fit_transform(featureSet['country'])
    featureSet['file extension'] = le.fit_transform(featureSet['file extension'])
    

    y_pred_class = model.predict(featureSet.drop(['url', 'len of url', 'no of subdir'], axis = 1))

    y_pred_prob = model.predict_proba(featureSet.drop(['url', 'len of url', 'no of subdir'], axis = 1))

    y_pred_str = ''

    #if str(y_pred_class.item()) == '1':
    if y_pred_prob[0][1] >= 0.6:
        y_pred_str = 'The url is malicious.'
        y_pred_binary = 1
    #elif str(y_pred_class.item()) == '0':
    else:
        y_pred_str = 'The url is benign.'
        y_pred_binary = 0

    with open(pred_out,'w') as file:
        file.write(y_pred_str)

    return(y_pred_str, y_pred_prob[0][1], y_pred_binary)

def run_prediction(args):
    with open(args.config, 'r') as f:
        config = yaml.load(f)
    RF = readModel(**config['prediction']['readModel'])
    url = args.url
    featureSet = generateFeature(url)
    featureSet.to_csv('test.csv')
    getPrediction(RF, featureSet, **config['prediction']['getPrediction'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Make Predictions')
    parser.add_argument('--config', '-c', default = 'config.yml', help='path to yaml file with configurations')
    parser.add_argument('--url', help = 'url to be predicted')
    args = parser.parse_args()

    run_prediction(args)
