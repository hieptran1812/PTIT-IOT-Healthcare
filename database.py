from flask import Flask
from flask_pymongo import pymongo

username = "customer_db"
password = "hiep1812"
database_name = "ptit-wav2vec"

CONNECTION_STRING = "mongodb+srv://" + username + ":" + password + "@cluster0.dv4jr.mongodb.net/" + database_name + "?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database(database_name)
