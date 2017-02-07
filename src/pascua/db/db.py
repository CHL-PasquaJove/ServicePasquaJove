from pymongo import MongoClient
import pascua.config as config

pascuadb = MongoClient(config.url)[config.database]
