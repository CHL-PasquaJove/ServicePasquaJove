from pymongo import MongoClient
import os

database = 'pasquajove'
if 'OPENSHIFT_MONGODB_DB_URL' in os.environ:
    url = os.environ['OPENSHIFT_MONGODB_DB_URL']
else:
    url = "mongodb://127.0.0.1:27017/"

pascuadb = MongoClient(url)[database]
