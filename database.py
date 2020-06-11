# Import credentials from config.py file (added to .gitignore)
from config import mongoCredentials

from bson import ObjectId # For ObjectId to work
from pymongo import MongoClient

class Database:
    def __init__(self):
        self.client = MongoClient(mongoCredentials['connectionString'])
        self.db = self.client.test
        self.curatorCollection = self.db.curators

    def insertProduct(self, product):
        self.curatorCollection.insert_one(product)
        return 'Inserted product into db'

