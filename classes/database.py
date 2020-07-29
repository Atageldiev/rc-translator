# ---------------------------------------------------------------------------
#   imports
# ---------------------------------------------------------------------------
import logging

from aiogram.types import User
from pymongo import MongoClient

from data.config import DB_USER, DB_PASS, DB_DB


# Class to work with database


class Database:
    """Class to work with DB"""
    __slots__ = ["collection"]

    def __init__(self):
        cluster = MongoClient(
            f"mongodb+srv://{DB_USER}:\
{DB_PASS}@rc-translator.d217k.mongodb.net/\
{DB_DB}?retryWrites=true&w=majority")

        db = cluster["rc-translator"]
        self.collection = db["status"]

    def user_id_exists(self):
        """Checks if the user is already in DB, adds if he is not"""
        user = User.get_current()

        name = user.first_name
        user_id = user.id

        if not self.collection.find_one(
                {
                    "_id": user_id
                }
        ):
            self.collection.insert_one(
                {
                    # user-info:
                    "_id": user_id,
                    "name": name,
                    # status:
                    "subbed": True,  # represents user's subscription status
                    "learning_mode": 1,  # represents chosen learning mode
                    # rating:
                    "words_translated": 0,  # represents how many words user has translated
                    "grammar_used": 0,  # represents how many times user has used /grammar command
                    "word_id": 0
                }
            )
            logging.info("User has been added")

    def get_user_ids(self):
        """
        
        Returns a list of all user_ids found in DB 
        
        """
        data = self.collection.find({})
        return [x["_id"] for x in data]

    def get_value(self, name: str):
        """
        
        Returns requested column's value
        :params:
        :name:str:name of column
        """
        user = User.get_current()
        user_id = user.id

        data = self.collection.find_one({"_id": user_id})

        return data[name]

    def update_value(self, name: str, value: any = None):
        """
        
        Update any value in the DB
            In case value is provided, sets that value
            If not, increments value(+1)
        
            Func defines current user_id itself
        
        """
        user = User.get_current()
        user_id = user.id

        if value is not None:  # if value is provided, sets that value
            self.collection.update_one(
                {
                    "_id": user_id
                },
                {
                    "$set":
                        {
                            name: value
                        }
                }
            )
            return

        self.collection.update_one(  # if there is no value provided, increments value(+1)
            {
                "_id": user_id
            },
            {
                "$inc":
                    {
                        name: 1
                    }
            }
        )

    def delete_all(self):
        """
        
        Delete everything in DB
        
        """
        self.collection.delete_many({})


class LearnerAPI(Database):

    def get_certain_mode_subs(self, mode):
        """

        Returns a list of user_ids of users that are subbed

        """
        data = self.collection.find(
            {
                "learning_mode": mode,
                "subbed": True
            }
        )
        return [x["_id"] for x in data]

    def get_word_id(self):
        return self.collection.find_one()["word_id"]

    def update_word_id(self):
        self.collection.update_one({}, {"$inc": {"word_id": 1}})
