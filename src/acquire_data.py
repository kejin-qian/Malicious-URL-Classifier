import pandas as pd
import numpy as np
import io
import urllib.request

"""
Warning: Running acquire_data takes a lot of time, majestic_million.csv ~80Mb
"""

def acquire_data():
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
	urllib.request.urlretrieve('http://data.phishtank.com/data/online-valid.csv', 'data/MaliciousURL.csv')
	urllib.request.urlretrieve('http://downloads.majestic.com/majestic_million.csv', 'data/GoodURL.csv')
	urllib.request.urlretrieve('https://raw.githubusercontent.com/incertum/cyber-matrix-ai/master/Malicious-URL-Detection-Deep-Learning/data/url_data_mega_deep_learning.csv', 'data/GithubURL.csv')

def create_project_data():
	"""
	Create the project dataset from MaliciousURL.csv and GoodURL.csv.

	The malicious dataset only contains 13854 malicious urls, to create a balanced dataset, only select
	top 13854 good urls from GoodURL.csv. 20000 URLs are randomly selected from GithubURL.csv. Drop dupliates.

	Output: 
	project_data.csv created in the data folder
	"""

	# Load datasets from local
	URL_good = pd.read_csv('data/GoodURL.csv')
	URL_bad = pd.read_csv('data/MaliciousURL.csv')
	urldata = pd.read_csv('GithubURL.csv')

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
	URL_selected_all.to_csv('data/project_data.csv')




if __name__ == "__main__":
	acquire_data();
	create_project_data()