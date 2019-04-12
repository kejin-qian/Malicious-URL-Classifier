# Malicious/Secure URL Classifier Using URL Strings

* **Developer**: [Kejin Qian](https://github.com/kejin-qian)
* **QA**: [Sophie Du](https://github.com/chuandu2)
----------------------------------------------------------------
<!-- toc -->

- [Project Charter](#project-charter)
	* [Mission](#mission)
	* [Vision](#vision)
	* [Success Criteria](#success-criteria)
- [Planned Work](#planned-work)
* [Backlog](#backlog)
* [Icebox](#icebox)

<!-- tocstop -->

## Project Charter 

### **Vision**:

Increase Internet security by spotting malicious websites based on URL strings provided by users.

### **Mission**:

To improve the efficiency of malice detection by enabling users to identify malicious URLs prior to downloading the webpage or crawling page contents. This goal will be achieved by building a Machine-Learning predictive model using features extracted from the URL strings and information about the host based on features queried from WHOIS server. User input URLs will be added to internal database and predictive model will be re-trained in a timely basis using updated database to improve prediction accuracy.

### **Success criteria**:

Successfully build a Machine Learning predictive model that dynamically classifies user-provided URL string(s) into Malicious/Secure class(es) with a F-measure greater than 0.85 and AUC higher than 0.7. 

Collect 100 URLs from users and add them into URL database with corresponding classification results. Re-train the predictive model in a timely basis using updated database.


## Planned Work


### **Theme1**: 
Identify various patterns, text attributes and Host-based features that are hidden in URL strings but could be significant in spotting malicious URLs. 

**Epic1 - Data Acquisition** <*Next Two Weeks*>

A URL database will be first built by collecting a large amount of malicious and secure URLs from various sources.

- **Story 1**: Aggregate lists of verified malicious urls from [Phishtank] (https://www.phishtank.com/) and lists of secure urls from various URL whitelist databases.(1 point)
    
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
Obtain reliable Machine Learning predictive model of classifing single or multiple URL(s) provided by user into Malicious or Secure URL(s) based on features extracted primarily from the URL string(s). The reliability of the model is evaluated based on the performance metrics F-measure and AUC.

**Epic1 - Malicious/Secure URL classification**

A set of machine learning predictive models will be built, a 10-fold cross validation will be applied to each model to evaluate model performance. Final model selection will be made based on the results.

- **Story 1**: Build, train, tune(via Cross Validate) each potential candidates of classification algorithms. Potential algorithms are: Decision Trees, Random Forest, AdaBoost, GradientBoosting, GaussianNB and Logistic Regression. For each algorithm, select the optimal model using the best set of parameters found, report cross validation classification accuracy, F-measure and AUC. (8 points)

- **Story 2**: Final Model Selection: Classification accuracy, F-measure and AUC are possible machine learning performance metrics for the classifiers built above. To optimize precision(how many predicted malicious urls are actually malicious) and recall(how many malicious urls identified correctly by model), F-measure and AUC will be the primary performance metric. The final best model selected will be the one with the highest F-measure and the highest AUC. (4 points)

- **Story 3**: Build a stacked predictive model using optimal models found in S1 to improve the classifier’s predictive power. Compare the performance metric of the stacked model with the final best model selected in S2 and choose the winner.(4 points)


### **Theme3**:
Deploy an interactive and dynamic web application which takes URL(s) from user and provide Malicious/Secure classification as output with statistics and explanations supporting the decision. Build URL database using the training data and update it with user inputs and corresponding classification results. Re-train the predictive model using latest database in a timely manner. 

**Epic1 - User Interface for detecting malicious URLs**

Build the Malicious URL Classifier using Flask, which takes single or multiple URL(s) as input and output the classification results and explanations.

- **Story 1**: Design the front end for user input: User are able to type in single url in text box or check multiple urls by selecting the number of urls they want to test and receive that number of text boxes in return. (4 points)

- **Story 2**: Features used in classification and their importance evaluated by the final best model will be listed and explained on the interface for users’ interests.(1 point)

- **Story 3**: Output interface design: The classification result ‘Secure’ or ‘Malicious’ will be the primary prediction output from the final best model. For malicious urls, explanations on why it is classified as malicious will be provided as output with the classification result(Examples:existence of @ in subdomain, using IP address to substitute domain, etc). (4 points)

- **Story 4**: Build the Malicious URL Classifier web app using tools, libraries and technologies provided by **Flask**.(8 points)

- **Story 5**: Setup **Amazon cloud server AWS S3** for file hosting; to store files/information that can’t be stored in a relational database.(4 points)


**Epic2 - More interactive display of Malicious URL Classifier**

Build a dynamic web application by re-train the model regularly using a dynamic URL database and output more interactive analyses based on user's input.

- **Story 1**: Build a dynamic database which can be initialized using training set of the malicious and secure URLs and updated in real time using user input and predicted outcome. The final best model will be re-trained using the updated URL database in a timely manner to improve classification performance and accuracy.(8 points)
    
- **Story 2**: Interactive interface to preview the webpage within the web app if the webpage’s URL is classified as Secure.(2 points)

- **Story 3**: Output visualizations of features extracted from the URL provided by the user against the distributions of that feature of all the malicious and secure URLs stored in database, This can also give users intuitions on why the URLs they provided are identified as Malicious/Secure.(4 points)

### Backlog
1. ***Theme1.Epic1.Story1***: Collect URL lists (1 point) - **Planned**
2. ***Theme1.Epic1.Story2***: Quality check on URL lists (2 points) - **Planned**
3. ***Theme1.Epic2.Story1***: URL stings' Feature Exploration (4 points) - **Planned**
4. ***Theme1.Epic2.Story2***: Host-based feature from WHOIS Server (4 points) - **Planned**
5. ***Theme1.Epic2.Story3***: Visualizations on features' distributions for Malicious&Secure URLs (2 points) - **Planned**
6. ***Theme1.Epic3.Story1***: Exploratory Data Analysis (4 points) - Planned
7. ***Theme2.Epic1.Story1***: Classification Model Building and Hyper Parameter Selection (8 points) - **Planned**
8. ***Theme2.Epic1.Story2***: Final Model Selection (4 points)
9. ***Theme3.Epic1.Story1***: Front End Design (4 points)
10. ******Theme3.Epic1.Story2***: Feature Importance Presentaiton (1 point)
11. ***Theme3.Epic1.Story3***: Output Interface Design (4 points)
12. ***Theme3.Epic1.Story4***: Web App Construction (8 points)
13. ***Theme3.Epic1.Story5***: Transfer from Local to Server (4 points)
14. ***Theme3.Epic2.Story1***: Dynamic URL Database (8 points)

### **Icebox**
1. ***Theme2.Epic1.Story3***: Stacked Model Building (4 points)
2. ***Theme3.Epic2.Story2***: Secure Webpage Preview (2 points)
3. ***Theme3.Epic2.Story3***: Output Visualizations to Support Classification Decision (4 points)



