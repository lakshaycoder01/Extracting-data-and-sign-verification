from pymongo import MongoClient
from flask import jsonify
try:
    client = MongoClient()
    print("Connected Successfully")
except:
    print('There is problem in connection')


def database_config():
    db = client['customer_2']
    db_coll = db['collection']
    return db_coll
