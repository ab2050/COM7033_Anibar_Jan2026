from pymongo import MongoClient as mongc
import os
from dotenv import load_dotenv
from datetime import datetime
from bson.objectid import ObjectId # binary JSON, needed to decode mongoDB object ids
import atexit

load_dotenv()
user = os.getenv("mongouser")
pwd = os.getenv("mongopass")

def connector():
    mongo = mongc(f"mongodb://{user}:{pwd}@localhost:27017/")
    return mongo

mongo = connector()
db = mongo["health_management"]
patdata = db["patients"]
atexit.register(mongo.close)

def patientAddsData(username,name,age):
    patdata.update_one(
        {"_id":username},
        {
            "$set":{
                "name":name,
                "age":age,
                "updatedOn":datetime.now()
            },
            "$setOnInsert":{
                "createdOn":datetime.now()
            }
        },upsert=True) # will only create one record per id

def medAddsData(data):
    val = {
        "name":data.get("name"),
        "age":data.get("age"),
        "disease":data.get("disease"),
        "medicines":data.get("medicines"),
        "notes":data.get("notes"),
        "createdOn":datetime.now(),
        "updatedOn":datetime.now()
    }
    return patdata.insert_one(val)

def showpatients():
    return list(patdata.find())

def individual(username):
    return patdata.find_one({"_id":username})