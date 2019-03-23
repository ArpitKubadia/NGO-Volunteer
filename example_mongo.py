'''from flask_pymongo import PyMongo

app.config['MONGO_DBNAME']='mongo_online'
app.config['MONGO_URI']='mongodb+srv://arpitkubadia:arpit%40123@cluster0-rpcm0.mongodb.net/admin'

mongo=PyMongo(app)

users=mongo.db.users

users.insert({'name':'Arpit','password':'arpit123'})
'''
import pymongo

client = pymongo.MongoClient("mongodb+srv://arpitkubadia:<password>@cluster0-rpcm0.mongodb.net/test?retryWrites=true")
db = client.test


