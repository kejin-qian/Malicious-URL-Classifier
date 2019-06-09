.PHONY: acquire_data data_prep encoding training evaluation prediction

data/project_data.csv: config/config.yml 
	pythonw src/acquire_data.py --config=config/config.yml

acquire_data: data/project_data.csv 

data/FeatureData.csv: config/config.yml data/project_data.csv 
	pythonw src/data_prep.py --config=config/config.yml --opt_length=100

data_prep: data/FeatureData.csv 

data/ModelfeatureSet.csv: config/config.yml data/FeatureData.csv
	pythonw src/encoding.py --config=config/config.yml 

encoding: data/ModelfeatureSet.csv data/modelLabel.csv

model/randomForest.pkl: config/config.yml data/ModelfeatureSet.csv data/modelLabel.csv
	pythonw src/training.py --config=config/config.yml 

training: model/randomForest.pkl

evaluation/ConfusionMatrix.csv: config/config.yml model/randomForest.pkl data/ModelfeatureSet.csv data/modelLabel.csv data/FeatureData.csv
	pythonw src/evaluation.py --config=config/config.yml 

evaluation: evaluation/ConfusionMatrix.csv \
			image/confusion_matrix.png \
			image/probHist.png \
			image/ROC.png \
			evaluation/Model_evaluation_output.txt \
			evaluation/feature_rank.txt 

prediction/predicted_class.txt: config/config.yml model/randomForest.pkl
	pythonw src/prediction.py --config=config/config.yml --url=www.expedia.com

prediction: prediction/predicted_class.txt 

clean-files:
	rm data/ModelfeatureSet.csv
	rm data/modelLabel.csv
	rm model/randomForest.pkl
	rm model/classes.npy
	rm evaluation/ConfusionMatrix.csv
	rm image/confusion_matrix.png
	rm image/probHist.png
	rm image/ROC.png
	rm evaluation/Model_evaluation_output.txt
	rm evaluation/feature_rank.txt
	rm prediction/predicted_class.txt 



all: | acquire_data data_prep encoding training evaluation prediction