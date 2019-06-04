import pandas as pd
import numpy as np
import io
import urllib.request
import logging
import argparse
import yaml
import boto3
s3 = boto3.client("s3")
"""
Warning: Running acquire_data takes several minutes to run, majestic_million.csv ~80Mb
"""

logging.basicConfig(filename='malicious_url.log', filemode='a',
                    level=logging.DEBUG, format='%(name)s - %(levelname)s - %(asctime)s - %(message)s')
logger = logging.getLogger()

def acquire_data(bad_in, good_in, git_in, bad_out, good_out, git_out):
	"""
	Download csv datasets from source websites.
`	
	- http://data.phishtank.com/data/online-valid.csv contains 13854 malicious urls
	- http://downloads.majestic.com/majestic_million.csv contains top-visited 1 million websites
	  on the internet. 
	- https://raw.githubusercontent.com/incertum/cyber-matrix-ai/master/Malicious-URL-Detection-Deep-Learning/data/url_data_mega_deep_learning.csv
	  contains both good and bad URLs

	Output:
	MaliciousURL.csv and GoodURL.csv created in the data folder.

	"""
	# Download the file from urls and save it locally under specified file_name:
	urllib.request.urlretrieve(bad_in, bad_out)
	urllib.request.urlretrieve(good_in, good_out)
	urllib.request.urlretrieve(git_in, git_out)

def create_project_data(bad_in, good_in, git_in, project_data_out):
	"""
	Create the project dataset from MaliciousURL.csv and GoodURL.csv.

	The malicious dataset only contains 13854 malicious urls, to create a balanced dataset, only select
	top 13854 good urls from GoodURL.csv. 20000 URLs are randomly selected from GithubURL.csv. Drop dupliates.

	Output: 
	project_data.csv created in the data folder
	"""

	# Load datasets from local
	URL_good = pd.read_csv(good_in)
	URL_bad = pd.read_csv(bad_in)
	urldata = pd.read_csv(git_in)

    # randomly select 10k good urls and 10k malicious urls from both datasets and combine
	np.random.seed(1)
	url_bad = urldata[urldata['isMalicious'] == 1].sample(10000)
	url_good = urldata[urldata['isMalicious'] == 0].sample(10000)
	url_selected = url_bad.append(url_good)
	url_selected.columns = ['url', 'label']

	# create empty dataframes to store selected good and bad urls
	URL_selected_good = pd.DataFrame(columns=['url', 'label'])
	URL_selected_bad = pd.DataFrame(columns=['url', 'label'])

    # label all the good urls 0
	URL_selected_good['url'] = URL_good['Domain']
	URL_selected_good['label'] = 0

	# label all the malicious urls 1
	URL_selected_bad['url'] = URL_bad['url']
	URL_selected_bad['label'] = 1

	# combine all the parts together and drop duplicates
	URL_selected_all = URL_selected_bad.append(URL_selected_good.head(URL_selected_bad.shape[0])).append(url_selected)
	URL_selected_all = URL_selected_all.reset_index(drop=True)
	URL_selected_all = URL_selected_all.drop_duplicates(subset=['url'])

	# save project dataset to local
	URL_selected_all.to_csv(project_data_out)

def UploadFile(input_path1, input_path2, input_path3, input_path4, bucket_name, output_path1, output_path2, output_path3, output_path4):
    """
    Upload one file from Local to S3 bucket.

    """
    s3.upload_file(input_path1, bucket_name, output_path1)
    s3.upload_file(input_path2, bucket_name, output_path2)
    s3.upload_file(input_path3, bucket_name, output_path3)
    s3.upload_file(input_path4, bucket_name, output_path4)

def run_acquire_data(args):
    '''acquire data from the command line'''
    with open(args.config, 'r') as f:
        config = yaml.load(f)

    acquire_data(**config['acquire_data']['acquire_data'])
    create_project_data(**config['acquire_data']['create_project_data'])
    UploadFile(**config['acquire_data']['UploadFile'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Acquire data from web')
    parser.add_argument('--config', '-c', default = 'config.yml', help='path to yaml file with configurations')
    args = parser.parse_args()

    run_acquire_data(args)
