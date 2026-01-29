"""
User DAO (Data Access Object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from models.product import Product

class ProductDAOMongo:
    def __init__(self):
        try:
            env_path = ".env"
            print(os.path.abspath(env_path))
            load_dotenv(dotenv_path=env_path)
            db_host = os.getenv("MONGO_HOST")
            db_name = os.getenv("MONGO_DB_NAME")
            db_user = os.getenv("DB_USERNAME")
            db_pass = os.getenv("DB_PASSWORD") 
            self.client = MongoClient(
                f"mongodb://{db_user}:{db_pass}@{db_host}:27017"
            )
            db = self.client[db_name]
            self.collection = db["products"] 
            
        except FileNotFoundError as e:
            print("Attention : Veuillez créer un fichier .env")
        except Exception as e:
            print("Erreur : " + str(e))

    def select_all(self):
        """ Select all users from MySQL """
        rows = self.collection.find()
        return [
        Product(
            prod_id=row.get("_id"),
            name=row.get("name"),
            brand=row.get("brand"),
            price=row.get("price")
        )
        for row in rows
        ]

    def insert(self, prod):
        """ Insert given user into MySQL """
        return self.collection.insert_one({"name" :prod.name, "brand" : prod.brand, "price" : prod.price}).inserted_id

    def update(self, prod):
        """ Update given user in MySQL """
        self.collection.find_one_and_update(
            {"_id" : prod.prod_id}, 
            {"$set":{"name" :prod.name, "brand" : prod.brand, "price" : prod.price}}
            )
        

    def delete(self, prod_id):
        """ Delete user from MySQL with given user ID """
        self.collection.find_one_and_delete({"_id" : prod_id})
        
        

    def delete_all(self): #optional
        """ Empty users table in MySQL """
        self.collection.delete_many( {})
        
        
        
    def close(self):
        self.client.close()
