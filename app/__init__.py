#app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

# Initialize the Flask application
application = Flask(__name__)

# Configure flask app from config.py
application.config.from_object('config')

# Initialize the database
db = SQLAlchemy(application)