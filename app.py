#ex1

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return jsonify({"message": "Hello world, this is my first web API!"})

if __name__ == '__main__':
    app.run(debug=True)

#ex2
    
from pymongo import MongoClient
import json
from bson import json_util


def laureates():
    
    client = MongoClient("mongodb://localhost:27017/")
    db = client["nobel_database"] 
    collection = db["laureates"]    
    cursor = collection.find()

    laureates_list = list(cursor)

    sorted_laureates = sorted(
        laureates_list,
        key=lambda x: (x.get("date", ""), x.get("family_name", ""))
    )

    return json.dumps(sorted_laureates, default=json_util.default)

#ex2bis

from pymongo import MongoClient
import json
from bson import json_util

def prizes():

    client = MongoClient("mongodb://localhost:27017/")
    db = client["nobel_database"]  
    collection = db["prizes"]      
    cursor = collection.find()

    prizes_list = list(cursor)

    sorted_prizes = sorted(
        prizes_list,
        key=lambda x: (x.get("date", ""), x.get("category", "")),
        reverse=False
    )

    sorted_prizes.sort(key=lambda x: x.get("category", ""), reverse=True)

    return json.dumps(sorted_prizes, default=json_util.default)

#ex3

from pymongo import MongoClient
import json
from bson import json_util
from fastapi import FastAPI, Query

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["nobel_database"]  
laureates_collection = db["laureates"]

@app.get("/laureates")
def laureates(category: str = Query(None)):
    query = {}
    if category:
        query["category"] = category

    cursor = laureates_collection.find(query)

    laureates_list = list(cursor)

    sorted_laureates = sorted(
        laureates_list,
        key=lambda x: (x.get("date", ""), x.get("family_name", ""))
    )

    return json.dumps(sorted_laureates, default=json_util.default)

prizes_collection = db["prizes"]

@app.get("/prizes")
def prizes(awarded: int = Query(None)):
   
    query = {}
    if awarded == 1:
        query["laureates"] = {"$exists": True, "$ne": []}  
    elif awarded == 0:
        query["laureates"] = {"$exists": False}  

    cursor = prizes_collection.find(query)

    prizes_list = list(cursor)

    sorted_prizes = sorted(
        prizes_list,
        key=lambda x: (x.get("date", ""), x.get("category", "")),
        reverse=False
    )
    sorted_prizes.sort(key=lambda x: x.get("category", ""), reverse=True)

    return json.dumps(sorted_prizes, default=json_util.default)

#ex4

from pymongo import MongoClient
import json
from bson import json_util
from fastapi import FastAPI, Query

app = FastAPI()

client = MongoClient("mongodb://localhost:27017/")
db = client["nobel_database"]  
laureates_collection = db["laureates"]

@app.get("/laureates")
def laureates(category: str = Query(None), awarded_year: str = Query(None)):
    
    query = {}
    if category:
        query["category"] = category
    if awarded_year:
        query["date"] = {"$regex": f"^{awarded_year}"}  

    cursor = laureates_collection.find(query)

    laureates_list = list(cursor)

    sorted_laureates = sorted(
        laureates_list,
        key=lambda x: (x.get("date", ""), x.get("family_name", ""))
    )

    return json.dumps(sorted_laureates, default=json_util.default)

prizes_collection = db["prizes"]

@app.get("/prizes")
def prizes(before: str = Query(None), after: str = Query(None), awarded: int = Query(None)):
   
    query = {}
    if awarded == 1:
        query["laureates"] = {"$exists": True, "$ne": []}  
    elif awarded == 0:
        query["laureates"] = {"$exists": False}  

    if before:
        query["date"] = {"$lte": before}  
    if after:
        if "date" not in query:
            query["date"] = {"$gte": after} 
        else:
            query["date"].update({"$gte": after})

    cursor = prizes_collection.find(query)

    prizes_list = list(cursor)

    sorted_prizes = sorted(
        prizes_list,
        key=lambda x: (x.get("date", ""), x.get("category", "")),
        reverse=False
    )
    sorted_prizes.sort(key=lambda x: x.get("category", ""), reverse=True)

    return json.dumps(sorted_prizes, default=json_util.default)

