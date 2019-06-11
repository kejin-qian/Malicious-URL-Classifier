# Malicious/Secure URL Classifier Using URL Strings

* **Developer**: [Kejin Qian](https://github.com/kejin-qian)
* **QA**: [Sophie Du](https://github.com/chuandu2)
----------------------------------------------------------------
<!-- toc -->

- [Project Charter](#project-charter)
	* [Vision](#vision)
	* [Mission](#mission)
	* [Success Criteria](#success-criteria)
- [Planned Work](#planned-work)
	* [Project Backlog](#project-backlog)
	* [Project Icebox](#project-icebox)
- [Repo structure](#repo-structure)
- [Documentation](#documentation)
- [Running the application](#running-the-application)
  *[0. Clone the project repo to local](#clone-project-repo)
  * [1. Set up environment](#1-set-up-environment)
  * [2. Reproduce the whole pipeline](#2-reproduce-pipeline)
  * [3. Configure Flask app](#3-configure-flask-app)
  * [4. Initialize the database](#4-initialize-the-database)
  * [5. Run the application](#5-run-the-application)
  * [6. Interact with the application](#6-interaction-with-app)
- [Testing](#testing)

<!-- tocstop -->

## Project Charter 

### **Vision**:

Increase Internet security and improve the efficiency of malice detection by spotting malicious websites based on URL strings provided by users without downloading the webpage or crawling page contents.

### **Mission**:

Classify URLs as Malicious or Secure using Machine-Learning predictive models based on features extracted primarily from the URL strings and Host-based features queried from WHOIS Server. User input URLs will be added to an internal URL database and the predictive model will be re-trained in a timely basis using updated database to improve prediction accuracy.

### **Success criteria**:

Successfully build a Machine Learning predictive model that dynamically classifies user-provided URL string(s) into Malicious/Secure class(es) with a F-score greater than 0.85 and AUC higher than 0.7. 

Collect 100 URLs from users and add them into URL database with the corresponding classification results. 
Re-train the predictive model in a timely basis using updated database and achieve better performance metrics.


## Planned Work


### **Theme1**: 
Identify various patterns, text attributes and Host-based features that are hidden in URL strings but could be significant in spotting malicious URLs. 

**Epic1 - Data Acquisition** 

A URL database will be first built by collecting a large amount of malicious and secure URLs from various sources.

- **Story 1**: Aggregate lists of verified malicious urls from [Phishtank](https://www.phishtank.com/) and lists of secure urls from various URL whitelist databases.(1 point)
    
- **Story 2**: Implement quality check on aggregated URL lists. In order to be prepared for any kinds of urls user may type in, comprehensive selections of URL types, lengths, extension are desired. Manually add extra urls if lack of any kind of urls is noticed. (2 points)


 **Epic2 - Feature Generation based on URL string** 
 
 Explore any patterns, text attributes and Host-based features that are hidden in URL strings that could be significant in detecting malicious URLs.

- **Story 1**: Explore on special characteristics that malicious URLs usually have, such as larger amount of dots appeared in sub domain, existence of @, using IP as the domain name, etc. Create features purely from URL strings for each URL based on the investigation results.(4 points)
    
- **Story 2**: Obtain Host based features of each URL by querying from **Whois Server**, such as create date, update date, expiration date, country-based, etc. For this query purpose the **PyWhois** module has been used.(4 points)

- **Story 3**: Create visualizations on distributions of each feature obtained of both malicious and secure urls. Enable users to see the significance of each feature on classifying malicious urls based on the aggregated url database.(2 points)


**Epic3 - Exploratory Data Analysis**  

Features collected from previous steps will be merged into a final dataset. Exploratory Data Analysis will be implemented on it.

- **Story 1**: Run descriptive statistics across all collected features and implement missing-data imputation. Initial feature selection, standardization and feature transformation can be implemented based on the summary statistics and visualizations prepared in the previous stage. (4 points)


### **Theme2**:
Obtain reliable Machine Learning predictive model of classifing single or multiple URL(s) provided by user into Malicious or Secure URL(s) based on features extracted primarily from the URL string(s). The reliability of the model is evaluated based on the performance metrics F-score and AUC.

**Epic1 - Malicious/Secure URL classification**

A set of machine learning predictive models will be built, a 10-fold cross validation will be applied to each model to evaluate model performance. Final model selection will be made based on the results.

- **Story 1**: Build, train, tune(via Cross Validate) each potential candidates of classification algorithms. Potential algorithms are: Decision Trees, Random Forest, AdaBoost, GradientBoosting, GaussianNB and Logistic Regression. For each algorithm, select the optimal model using the best set of parameters found, report cross validation classification accuracy, F-score and AUC. (8 points)

- **Story 2**: Final Model Selection: Classification accuracy, F-score and AUC are possible machine learning performance metrics for the classifiers built above. To optimize precision(how many predicted malicious urls are actually malicious) and recall(how many malicious urls identified correctly by model), F-score and AUC will be the primary performance metric. The final best model selected will be the one with the highest F-score and the highest AUC. (4 points)

- **Story 3**: Build a stacked predictive model using optimal models found in S1 to improve the classifier’s predictive power. Compare the performance metric of the stacked model with the final best model selected in S2 and choose the winner.


### **Theme3**:
Deploy an interactive and dynamic web application which takes URL(s) from user and provide Malicious/Secure classification as output with statistics and explanations supporting the decision. Build URL database using the training data and update it with user inputs and corresponding classification results. Re-train the predictive model using latest database in a timely manner. Finally create Cloud infrastructure and move App to Cloud.

**Epic1 - Web Application Development and User Experience Design**

Build the Malicious URL Classifier using Flask and HTML, which takes single or multiple URL(s) as input and output the classification results and explanations. Set up an internal URL database using training data and URLs provided by users for future trainings. Extra interactive functions may be added to the App to improve user experience.

- **Story 1**: Design the front end for user input: Users are able to type in single url in text box or check multiple urls by selecting the number of urls they want to test and receive that number of text boxes in return. (4 points)

- **Story 2**: Output interface design: The classification result ‘Secure’ or ‘Malicious’ will be the primary prediction output from the final best model. For malicious urls, explanations on why it is classified as malicious will be provided as output with the classification result(Examples:existence of @ in subdomain, using IP address to substitute domain, etc). Features used in classification and their importance evaluated by the final best model will be listed and explained on the interface for users’ interests. (4 points)

- **Story 3**: Build a dynamic database which can be initialized using training set of the malicious and secure URLs and updated in real time using user input and predicted outcome. The final best model will be re-trained using the updated URL database in a timely manner to improve classification performance and accuracy.(8 points)

- **Story 4**: Interactive interface to preview the webpage within the web app if the webpage’s URL is classified as Secure.

- **Story 5**: Output visualizations of features extracted from the URL provided by the user against the distributions of that feature of all the malicious and secure URLs stored in database, This can also give users intuitions on why the URLs they provided are identified as Malicious/Secure.

- **Story 6**: Build the Malicious URL Classifier web app using tools, libraries and technologies provided by **Flask** and **HTML**.(8 points)


**Epic2 - Final testing and Local to Cloud Transfer**

After finishing web application design using Flask and HTML, testing will be implemented on modeling and Web App(user interface) scripts. If all the testings are passed, Web Application will be transferred to Cloud and a final test will be done in the Cloud.(8 points) 


### Project Backlog
1. ***Theme1.Epic1.Story1***: Collect URL lists (1 point) - **Finished**
2. ***Theme1.Epic1.Story2***: Quality check on URL lists (2 points) - **Finished**
3. ***Theme1.Epic2.Story1***: URL stings' Feature Exploration (4 points) - **Planned**
4. ***Theme1.Epic2.Story2***: Host-based feature from WHOIS Server (4 points) - **Finished**
5. ***Theme1.Epic2.Story3***: Visualizations on features' distributions for Malicious&Secure URLs (2 points) - **Planned**
6. ***Theme1.Epic3.Story1***: Exploratory Data Analysis (4 points) - **Planned**
7. ***Theme2.Epic1.Story1***: Classification Model Building and Hyper Parameter Selection (8 points) - **Planned**
8. ***Theme2.Epic1.Story2***: Final Model Selection (4 points)
9. ***Theme3.Epic1.Story1***: Front End Design (4 points)
10. ***Theme3.Epic1.Story2***: Output Interface Design (4 points)
11. ***Theme3.Epic1.Story3***: Dynamic URL Database (8 points)
12. ***Theme3.Epic1.Story6***: Web App Construction (8 points)
13. ***Theme3.Epic2***: Final Testing and Local to Cloud Transfer (8 points)

### **Project Icebox**
1. ***Theme2.Epic1.Story3***: Stacked Model Building
2. ***Theme3.Epic1.Story4***: Secure Webpage Preview
3. ***Theme3.Epic1.Story5***: Output Visualizations to Support Classification Decision

## Repo structure 

```
├── README.md                         <- You are here
│
├── app
│   ├── static/                       <- CSS, JS files that remain static 
│   ├── templates/                    <- HTML (or other code) that is templated and changes based on a set of inputs
│   ├── models.py                     <- Creates the data model for the database connected to the Flask app 
│   ├── __init__.py                   <- Initializes the Flask app and database connection
│
├── config                            <- Directory for yaml configuration files for model training, scoring, etc
│   ├── logging/                      <- Configuration files for python loggers
│
├── data                              <- Folder that contains data used or generated. Only the external/ and sample/ subdirectories are tracked by git. 
│   ├── archive/                      <- Place to put archive data is no longer usabled. Not synced with git. 
│   ├── external/                     <- External data sources, will be synced with git
│   ├── sample/                       <- Sample data used for code development and testing, will be synced with git
│
├── docs                              <- A default Sphinx project; see sphinx-doc.org for details.
│
├── figures                           <- Generated graphics and figures to be used in reporting.
│
├── models                            <- Trained model objects (TMOs), model predictions, and/or model summaries
│   ├── archive                       <- No longer current models. This directory is included in the .gitignore and is not tracked by git
│
├── notebooks
│   ├── develop                       <- Current notebooks being used in development.
│   ├── deliver                       <- Notebooks shared with others. 
│   ├── archive                       <- Develop notebooks no longer being used.
│   ├── template.ipynb                <- Template notebook for analysis with useful imports and helper functions. 
│
├── src                               <- Source data for the project 
│   ├── archive/                      <- No longer current scripts.
│   ├── helpers/                      <- Helper scripts used in main src files 
│   ├── sql/                          <- SQL source code
│   ├── add_songs.py                  <- Script for creating a (temporary) MySQL database and adding songs to it 
│   ├── ingest_data.py                <- Script for ingesting data from different sources 
│   ├── generate_features.py          <- Script for cleaning and transforming data and generating features used for use in training and scoring.
│   ├── train_model.py                <- Script for training machine learning model(s)
│   ├── score_model.py                <- Script for scoring new predictions using a trained model.
│   ├── postprocess.py                <- Script for postprocessing predictions and model results
│   ├── evaluate_model.py             <- Script for evaluating model performance 
│
├── test                              <- Files necessary for running model tests (see documentation below) 

├── run.py                            <- Simplifies the execution of one or more of the src scripts 
├── app.py                            <- Flask wrapper for running the model 
├── config.py                         <- Configuration file for Flask app
├── requirements.txt                  <- Python package dependencies 
```
This project structure was partially influenced by the [Cookiecutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/).

## Documentation
 
* Open up `docs/build/html/index.html` to see Sphinx documentation docs. 
* See `docs/README.md` for keeping docs up to date with additions to the repository.

## Running the application 

### 0. Clone the project repo to local
```
git clone https://github.com/kejin-qian/Malicious-URL-Classifier.git
```

### 1. Set up environment 
The `requirements.txt` file contains the packages required to run the model code. An environment can be set up after you cd to the repo path. 

#### (a). With `conda`
```bash
conda create -n URL_Classifier python=3.6
conda activate URL_Classifier
pip install -r requirements.txt
```

#### (b). Install python.app
To make sure all packages (especially matplotlib and seaborn) to work properly, please install python.app using the following command.
```bash
conda install python.app
```
After installing python.app, please use ```pythonw``` instead of ```python``` when run python scripts

### 2. Reproduce the whole pipeline
Before reproducing the project, please ensure that you have configured your AWS account by adding your credentials by ```aws configure```
Reproduce the project pipeline from acquiring source datasets from websites to making a single prediction.
The feature generation step ```data_prep.py``` takes a huge amount of time to query WHOIS server to acquire domain-related features. 

So currently, after cd to the cloned repo folder, running 

```make all``` 

in terminal can reproduce the pipeline by only generating features for the first 50 urls and build the model and make predictions based on these 50 urls. 
* All the source datasets downloaded will be saved to my public S3 bucket. 
* If you want to change the paths where all files, images, models will be saved to, please change the paths in ```config/config.yml```

You can choose how many urls you want to use to generate features by changing the ```opt_length``` arugument in line 9 ```pythonw src/data_prep.py --config=config/config.yml --opt_length=50``` in the ```makefile```. You can also choose to generate features for the whole URL dataset which contains more than 47,000 urls by changing line 9 to ```pythonw src/data_prep.py --config=config/config.yml```. 
* Generating features for the complete URL dataset needs about 8 hours. 

To run the rest of the pipeline(data cleaning, model training, evaluation and prediction) on the full dataset, please do the following (assume you have run ```make all``` and reproduced the pipeline using a subset of the urls 50 or a number of your choice)

```bash
# delete the files generated by running the whole pipeline using 50 urls, only keep source datasets in the data folder so that after downloading the full feature set from my S3 bucket, you can continue to run the rest of the pipeline

make clean-files

# download the complete feature set from my public S3 bucket

pythonw src/download_file.py --path_of_object_to_download=ProjectData/Complete_Feature_Set.csv --bucket_name=nw-kejinqian-s3 --output_file_path=data/FeatureData.csv

# reproduce the encoding step on the full feature data
make encoding

# reproduce model training step
make training

# reproduce model evaluation step
make evaluation

# reproduce the prediction step 
make prediction
```

### 3. Configure Flask app
`config.py` in the cloned repo folder holds the configurations for the Flask app. It includes the following configurations:
```python
DEBUG = True  # Keep True for debugging, change to False when moving to production 
LOGGING_CONFIG = "config/logging/local.conf"  # Path to file that configures Python logger
PORT = 3000  # What port to expose app on 
SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/url.db'  # URI for database that contains user input url and prediction result
```

### 4. Initialize the database
To create the database in the location configured in `config.py`, cd to the cloned repo folder, run:
 ```python
pythonw create_db.py
 ```

### 5. Run the application
cd to cloned repo folder first
if you want to run the app locally and create the database locally using sqlite db, keep the following line uncommented in config.py and comment out the line SQLALCHEMY_DATABASE_URI="{conn_type}://{user}:{password}@{host}:{port}/{DATABASE_NAME}
 ```bash
SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/url.db'
 ```

if you want to run on RDS, first make sure your your RDS is configured in the environment, then uncomment the following line in config.py and comment out the line SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/url.db
 ```bash
SQLALCHEMY_DATABASE_URI="{conn_type}://{user}:{password}@{host}:{port}/{DATABASE_NAME}"
 ```

Then you can run the app by
```bash
pythonw application.py 
 ```

### 6. Interact with the application 
Go to http://3.18.102.108:3000/ to interact with the current version of the application. 


## Testing 
cd to the cloned repo folder, run the following command lines in terminal
```
pythonw -m pytest test/tester.py
pythonw -m pytest test/test_feature_generation.py
```

Tests and datasets used for testing are stored in the test folder.


