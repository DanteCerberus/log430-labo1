"""
User DAO (Data Access Object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from models.user import User

class UserDAOMongo:
    def __init__(self):
        try:
            env_path = ".env"
            print(os.path.abspath(env_path))
            load_dotenv(dotenv_path=env_path)
            db_host = os.getenv("MYSQL_HOST")
            db_name = os.getenv("MYSQL_DB_NAME")
            db_user = os.getenv("DB_USERNAME")
            db_pass = os.getenv("DB_PASSWORD") 
            self.client = MongoClient(
                f"mongodb://{db_user}:{db_pass}@{db_host}:27017"
            )
            db = self.client[db_name]
            self.collection = db["users"] 
            
        except FileNotFoundError as e:
            print("Attention : Veuillez créer un fichier .env")
        except Exception as e:
            print("Erreur : " + str(e))

    def select_all(self):
        """ Select all users from MySQL """
        rows = self.collection.find()
        return [
        User(
            user_id=row.get("_id"),
            name=row.get("name"),
            email=row.get("email")
        )
        for row in rows
        ]

    def insert(self, user):
        """ Insert given user into MySQL """
        return self.collection.insert_one({"name" :user.name, "email" : user.email}).inserted_id

    def update(self, user):
        """ Update given user in MySQL """
        self.collection.find_one_and_update(
            {"_id" : user.id}, 
            {"$set":{"name" : user.name,"email" : user.email}}
            )
        

    def delete(self, user_id):
        """ Delete user from MySQL with given user ID """
        self.collection.find_one_and_delete({"_id" : user_id})
        
        

    def delete_all(self): #optional
        """ Empty users table in MySQL """
        self.collection.delete_many( {})
        
        
        
    def close(self):
        self.client.close()
