import os
import sys
import logging
import pandas as pd

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Text, Float
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy as sql

import argparse

logging.basicConfig(level=logging.DEBUG, filename="logfile", filemode="a+",
                        format="%(asctime)-15s %(levelname)-8s %(message)s")
logger = logging.getLogger('sql_db')

Base = declarative_base()


    
class Url_Prediction(Base):
    """
    Create a table to store user-input URLs.
    """
    
    __tablename__ = 'url_prediction'
    
    url = Column(String(100), primary_key=True, unique=True, nullable=False)
    
    # def __init__(self, url):
    #     self.url = url


class Url_features(Base):
    """
    Create a table to store all the url data and generated features.
    """
    
    __tablename__ = 'url_features'
    
    url = Column(String, primary_key=True, unique=True, nullable=False)
    no_of_dots = Column(Integer, unique= False, nullable=False)
    no_of_hyphen = Column(Integer, unique= False, nullable=False)
    len_of_url = Column(Float, unique= False, nullable=False)
    no_of_at = Column(Integer, unique= False, nullable=False)
    no_of_double_slash = Column(Integer, unique= False, nullable=False)
    no_of_subdir = Column(Integer, unique= False, nullable=False)
    no_of__subdomain = Column(Integer, unique= False, nullable=False)
    len_of_domain = Column(Integer, unique= False, nullable=False)
    no_of_queries = Column(Integer, unique= False, nullable=False)
    contains_IP = Column(Integer, unique= False, nullable=False)
    presence_of_suspicious_TLD = Column(Integer, unique= False, nullable=False)
    create_age = Column(Integer, unique= False, nullable=False)
    expiry_age = Column(Integer, unique= False, nullable=False)
    update_age = Column(Integer, unique= False, nullable=False)
    country = Column(String(100), unique= False, nullable=False)
    file_extension = Column(String(100), unique= False, nullable=False)
    risk_indicator = Column(Integer, unique= False, nullable=False)
    label = Column(Integer, unique= False, nullable=False)

    


def get_engine_string(RDS = False):
    if RDS:
        conn_type = "mysql+pymysql"
        user = os.environ.get("MYSQL_USER")
        password = os.environ.get("MYSQL_PASSWORD")
        host = os.environ.get("MYSQL_HOST")
        port = os.environ.get("MYSQL_PORT")
        DATABASE_NAME = 'msia423'
        engine_string = "{}://{}:{}@{}:{}/{}". \
            format(conn_type, user, password, host, port, DATABASE_NAME)
        # print(engine_string)
        logging.debug("engine string: %s"%engine_string)
        return  engine_string
    else:
        return 'sqlite:///url_classification.db'



def create_db(args,engine=None):
    """Creates a database with the data models inherited from `Base` (Tweet and TweetScore).

    Args:
        engine (:py:class:`sqlalchemy.engine.Engine`, default None): SQLAlchemy connection engine.
            If None, `engine_string` must be provided.
        engine_string (`str`, default None): String defining SQLAlchemy connection URI in the form of
            `dialect+driver://username:password@host:port/database`. If None, `engine` must be provided.

    Returns:
        None
    """
    if engine is None:
        RDS = eval(args.RDS)
        logger.info("RDS:%s"%RDS)
        engine = sql.create_engine(get_engine_string(RDS = RDS))

    Base.metadata.create_all(engine)
    logging.info("database created")




if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Create defined tables in database")
    parser.add_argument("--RDS", default="False",help="True if want to create in RDS else None")
    args = parser.parse_args()
    
    engine = create_db(args)

    # create engine
    engine = sql.create_engine(get_engine_string(RDS = True))
    
    # create a db session
    Session = sessionmaker(bind=engine)  
    session = Session()

    #INPUT user test
    input_url = Url_Prediction(url = 'www.google.com')
    session.add(input_url)
    session.commit()

    logger.info("New user input added")

    query = "SELECT * FROM url_prediction"
    df = pd.read_sql(query, con=engine)
    logger.info(df)
