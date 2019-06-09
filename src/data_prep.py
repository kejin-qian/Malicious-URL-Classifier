import os
import sys
import re
import matplotlib
import pandas as pd
import numpy as np
from os.path import splitext
import ipaddress as ip
import tldextract
import whois
import datetime
from urllib.parse import urlparse
import ipaddress as ip 
import iso3166
import logging
import argparse
import yaml

logging.basicConfig(filename='url_classifier.log', filemode='a', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger('data_prep')

def importData(path_in, random_state):
    """
    Import the project data from lcoal as Pandas DataFrame.

    Args:
        path_in(string): local path to the project dataset
        random_state(int): set seed to make sure this step is reproducible

    Return:
        URLdata(Pandas.DataFrame): Project dataset in Pandas DataFrame form
    """
    # load data in
    URLdata = pd.read_csv(path_in, index_col=0)
    # shuffle the dataset with a random state specified
    URLdata = URLdata.sample(frac=1, random_state = random_state).reset_index(drop=True)

    logging.info('top 5 rows of data:\n {}'.format(URLdata.head()))
    logging.info('shape of data: {}'.format(URLdata.shape))
    logging.info('There are {} rows in the data'.format(len(URLdata)))

    # find the dataset balance
    spam = len(URLdata[URLdata['label']==1])
    percent_spam = spam/len(URLdata)*100
    logging.info('There are {}  in the data'.format(len(URLdata)))

    return URLdata


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

#trend micro's top 30 malicious TLD
Suspicious_TLD=['zip','cricket','link','work','party','gq','kim','country','science','tk','download','xin','gdn',
                'racing','jetzt','stream','vip','bid','ren','load','mom','party','trade','date','wang','accountants',
               'bid','ltd','men','faith']
#trend micro's top 10 malicious domains 
Suspicious_Domain=['luckytime.co.kr','mattfoll.eu.interia.pl','trafficholder.com','dl.baixaki.com.br',
                   'bembed.redtube.comr','tags.expo9.exponential.com','deepspacer.com','funad.co.kr',
                   'trafficconverter.biz', 'alegroup.info']

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
    return len(url)

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

# create an empty feature set with all the columns needed
featureSet = pd.DataFrame(columns=('url','no of dots','no of hyphen','len of url','no of at',\
'no of double slash','no of subdir','no of subdomain','len of domain','no of queries','contains IP',
                                   'presence of Suspicious_TLD','create_age(months)','expiry_age(months)',
                                   'update_age(days)','country','file extension','label'))


def generateFeature(df, opt_length=None):
    """
    Generate features for the url dataset and store them into the featureSet dataframe.

    Args:
        df(Pandas.DataFrame): DataFrame for all the urls
        opt_length(default = None, integer): optional length. Number of urls selected to generate features.
                                         e.g. opt_length = 50, features will be generated for the first 50 urls in the dataset
                                              opt_length = None, features will be generated for the full URL dataset(~47000 urls)
    
    Return:
        None
    """

    size = len(df)
    # If opt_length(number of urls used to generate features) is passed in by the user, only generate features for the first opt_length urls
    # otherwise generate features for all the urls in the dataset.
    if opt_length:
        size = int(opt_length)
    for i in range(size):
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
    logger.debug('Features generated for {} urls.'.format(size))
    logger.debug('The shape of the feature set generated is {}'.format(featureSet.shape))

def getFeatures(url, label, w): 
    """
    Create features for each url string.

    Args:
        url(string): url string
        label(int): label indicates whether a url is malicious or not. 1 if it is malicious 0 otherwise 
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
            # appending updated age in days
        else:
            result.append(-1)

    
    #find the country that is hosting this domain
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
    result.append(str(label))
    return result


# If the URL is not registered on Whois, use getFeatures2
def getFeatures2(url, label): 
    """
    Create features for each url string.

    url(string): url string
    label(integer): label indicates whether a url is malicious or not. 1 if it is malicious 0 otherwise 

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
    
    #append label
    result.append(str(label))
    
    return result


def finalizeFeatures(featureSet, path_out):
    """
    Clean the FeatureSet and saved as csv to the specified path.

    Args:
        featureSet(Pandas.DataFrame): Generated feature set.
        path_out: path where the finalized featureSet should be saved to.
    """
    features = featureSet.columns.tolist()
    features.remove('url')
    features.remove('country')
    features.remove('file extension')
    for f in features:
        featureSet[f] = featureSet[f].astype(int)

    # Data Imputation by filling NA to the country and file extension column
    featureSet['country']=featureSet['country'].fillna('None')
    featureSet['file extension']=featureSet['file extension'].fillna('None')
    logger.info('The NAs in feature columns country and file extension have been filled with string None.')
    
    # clean country code
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

    ## Create a new feature called Risk Indicator
    c1 = featureSet['no of dots'] >= 1
    c2 = featureSet['no of hyphen'] >= 1
    c3 = featureSet['no of subdir'] >= 6
    c4 = featureSet['contains IP'] == 1
    c5 = featureSet['presence of Suspicious_TLD'] == 1

    featureSet['risk indicator'] = np.array([c1 | c2| c3| c4| c5]).astype(int).T
    logger.info('New feature Risk Indicator has been created!')
    featureSet.to_csv(path_out)
    logger.info('Feature Set has been saved to the data folder.')

def run_data_prep(args):
    '''Run of data prepration module from the command line'''
    with open(args.config, 'r') as f:
        config = yaml.load(f)

    URLdata = importData(**config['data_prep']['importData'])
    generateFeature(URLdata, opt_length = args.opt_length)
    finalizeFeatures(featureSet, **config['data_prep']['finalizeFeatures'])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Data Preparation')
    parser.add_argument('--config', '-c', default = 'config.yml', help='path to yaml file with configurations')
    parser.add_argument('--opt_length', default = None, help='size of data')
    args = parser.parse_args()

    run_data_prep(args)
