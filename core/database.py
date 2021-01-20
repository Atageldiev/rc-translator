from aiogram.types import User
from pymongo import MongoClient

from core.conf.settings import DATABASE


class Database:
    """Class to work with DB"""
    __slots__ = ["collection"]

    def __init__(self):
        cluster = MongoClient(f"mongodb+srv://"
                              f"{DATABASE.get('user')}:{DATABASE.get('password')}"
                              f"@rc-translator.d217k.mongodb.net/"
                              f"{DATABASE.get('db_name')}?retryWrites=true&w=majority")
        self.collection = cluster["rc-translator"]["status"]

    def user_exists(self):
        """Checks if the user is already in DB, adds if he is not"""
        user_id = self.user.id

        if not self.collection.find_one({"_id": user_id}):
            self.collection.insert_one(
                {
                    # user-info:
                    "_id": user_id,
                    "name": self.user.first_name,
                    # status:
                    "subbed": True,
                    "learning_mode": 1,
                    # rating:
                    "translated": 0,
                    "grammar_used": 0,
                })

    @property
    def user_ids(self):
        """Returns a list of all user_ids found in DB"""
        return [x["_id"] for x in self.collection.find({})]

    def clear(self):
        """Delete everything in DB"""
        self.collection.delete_many({})

    @property
    def user(self):
        return User.get_current()

    def __getattr__(self, item):
        data = self.collection.find_one({"_id": self.user.id})
        return data.get(item, "DATABASE ERROR!")

    def __setattr__(self, key, value):
        if key in self.__slots__:
            super(Database, self).__setattr__(key, value)
        else:
            self.collection.update_one({"_id": self.user.id}, {"$set": {key: value}})


db = Database()
