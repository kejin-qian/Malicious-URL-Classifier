from app import db
from app.models import URL
import os

'''
Creates a table in the database provided as the 'SQLALCHEMY_DATABASE_URI'
configuration parameter in __init__.py with the schema defined by models.URL()
'''

def create_db():
	db.create_all()
	print('database created')

if __name__ == "__main__":
	create_db()