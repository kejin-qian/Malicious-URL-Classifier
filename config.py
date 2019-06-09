import os
DEBUG = True
LOGGING_CONFIG = "config/logging/local.conf"
PORT = 3000
APP_NAME = "Malicious-URL-Classifier"
SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")


conn_type = "mysql+pymysql"
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
host = os.environ.get("MYSQL_HOST")
port = os.environ.get("MYSQL_PORT")
DATABASE_NAME = 'msia423'

#SQLALCHEMY_DATABASE_URI = 'sqlite:///../data/url.db'

# local: export SQLALCHEMY_DATABASE_URI='sqlite:///data/database/churn_prediction.db'
# rds: export SQLALCHEMY_DATABASE_URI="{conn_type}://{user}:{password}@{host}:{port}/{DATABASE_NAME}"

SQLALCHEMY_DATABASE_URI = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, DATABASE_NAME)

SQLALCHEMY_TRACK_MODIFICATIONS = True
HOST = "0.0.0.0"
