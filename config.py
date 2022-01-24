"""This module is to configure app to connect with database."""

from pymongo import MongoClient

#DATABASE = MongoClient()['UsersData'] # DB_NAME
DB_NAME = "song_db"
# DEBUG = True
client = MongoClient(host='test_mongodb',
                         port=27017,
                         username='root',
                         password='pass',
                        authSource="admin")
#db = client['song_db']

'''
client = MongoClient(host='test_mongodb',
                         port=27017,
                         username='root',
                         password='pass',
                        authSource="admin")
    db = client["song_db"]
'''