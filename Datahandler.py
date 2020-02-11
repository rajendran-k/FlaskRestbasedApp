import pymongo ,os
from pymongo import MongoClient

cluster = MongoClient(host='db', port=27017)
db= cluster['book']


def insert_data(data):
    collection = db["book"]
    collection.insert_one(data)

def search_data(data):
    datas ={}
    collection = db["book"]
    result = collection.find({"Isbn":data})   
    for ju in result:
        print(f"this is {ju}") 
        datas={
            "Name":ju["Name"],
            "Price":ju["Price"]
        }   
    
    if result is None:
        return False
    else:
        return datas   

def validate_isbn_exist(isbn):
    collection = db["book"]
    results = collection.find({"Isbn":isbn})
    for result in results:
        if result["Isbn"] == isbn:
            return True
    return False    

def update_data_using_isbn(isbn , model):
    if model is False:
        return False
    else:
        collection = db["book"]
        data_to_update = {"Isbn":isbn}
        model_to_update = {
            "Name":model["Name"],
            "Price":model["Price"]}
        collection.update_one(data_to_update,{ "$set": model_to_update })

def delete_data_using_isbn(isbn):
    if isbn is False:
        return False
    else:
        collection = db["book"]
        collection.delete_one({"Isbn":isbn})    
        return True

def get_all_data():
    collection = db["book"]
    i=0
    results = collection.find({})
    model = []    
    for result in results:
        model.insert(i, {"Name:": result["Name"],
        "Price": result["Price"],
        "Isbn": result["Isbn"]})       
        i = i+1
    return model    

def check_valid_user(username, passoword):    
    collection = db["users"]
    results = collection.find({"username":username})
    for result in results:
        if result["password"] == passoword:
            return True
    return False 

def user_is_present(username):
    collection = db["users"]
    results = collection.find({"username":username})
    for result in results:
        if result["username"] == username:
            return True
    return False

def add_user(username, password):
    if not username and password:
        return False
    else:
        collection = db["users"]
        collection.insert_one({'username':username,
        'password':password})
        return True






