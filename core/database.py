from aiogram.types import User
from pymongo import MongoClient

from core.settings import DATABASE


class Database:
    """Class to work with DB"""
    __slots__ = ["collection"]

    def __init__(self):
        cluster = self.__get_cluster(DATABASE.get("db_host"), DATABASE.get("user"), DATABASE.get("password"))
        self.collection = cluster["rc-translator"]["status"]

    @staticmethod
    def __get_cluster(db_host, user, password):
        return MongoClient(f"mongodb://{user}:{password}@localhost")

    def user_exists(self):
        """Checks if the user is already in DB, adds if he is not"""
        if not self.collection.find_one({"_id": self.user.id}):
            self.collection.insert_one(
                {
                    # user-info:
                    "_id": self.user.id,
                    "name": self.user.first_name,
                    # rating:
                    "translated": 0,
                    "grammar_used": 0,
                })

    @property
    def user_ids(self) -> list:
        """Returns a list of all user_ids found in DB"""
        return [x["_id"] for x in self.collection.find({})]

    def clear(self) -> None:
        """Delete everything in DB"""
        self.collection.delete_many({})

    @property
    def user(self) -> User:
        """Returns current user instance"""
        return User.get_current()

    def __getattr__(self, item):
        data = self.collection.find_one({"_id": self.user.id})
        return data.get(item, f"{item} does not seem to exist")

    def __setattr__(self, key, value):
        if key in self.__slots__:
            super(Database, self).__setattr__(key, value)
        else:
            self.collection.update_one({"_id": self.user.id}, {"$set": {key: value}})


db = Database()
