#---------------------------------------------------------------------------
#   imports
#---------------------------------------------------------------------------
import logging
import sqlite3

from aiogram.types import User

# Class to work with database


class Database():
    """This class is created to work with DB"""

    def __init__(self, database="data/server.db"):
        self.connection = sqlite3.connect(
            database=database, 
            check_same_thread=False
            )
        logging.info("Data base has been created")

        self.cursor = self.connection.cursor()
        logging.info("Cursor has been defined")

    def create_table_status(self):
        """Create table `status`"""
        with self.connection:
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS `status`(
                user_id INT,
                name STRING,
                words_translated INT DEFAULT 0,
                grammar_used INT DEFAULT 0,
                subbed BOOL DEFAULT False,
                learning_mode INT DEFAULT 1
                )
                """)
        logging.info("Table `status` has been created")

    def user_id_exists(self):
        """Checks if the user is already in DB, adds if he is not"""
        user = User.get_current()

        name = user.first_name
        user_id = user.id
        args = (user_id, name)

        with self.connection:
            self.cursor.execute(
                f"""SELECT `user_id` FROM `status` WHERE `user_id`={user_id}""")
            if self.cursor.fetchone() is None:
                self.cursor.execute(
                    f"""INSERT INTO `status`(user_id, name) VALUES (?, ?)""", args)
                logging.info(f"User {name} has been added to DB")

    def get_user_ids(self):
        """Get list of all `user_ids` in DB"""
        with self.connection:
            logging.info("User ids have been exported")
            return self.cursor.execute(f"""SELECT `user_id` FROM status""").fetchall()

    def get_value(self, name):
        """Get value from DB"""
        user = User.get_current()

        user_id = user.id
        args = (name, user_id)

        with self.connection:
            logging.info("Value has been exported")
            return self.cursor.execute(f"""SELECT {name} FROM `status` WHERE `user_id`={user_id}""").fetchone()[0]

    def get_subscribers(self):
        """Get list of subs, whose status `sub` is True"""
        with self.connection:
            logging.info("Subscribers list has been exported")
            return self.cursor.execute(f"""SELECT `user_id` FROM `status` WHERE `sub`=True""").fetchall()

    def update_value(self, name, value):
        """Update some value in DB"""
        user = User.get_current()
        user_id = user.id

        with self.connection:
            try:
                self.cursor.execute(
                    f"""UPDATE status SET {name}={value} WHERE `user_id`={user_id}""")
            except:
                self.cursor.execute(
                    f"""UPDATE `status` SET {name}='{value}' WHERE `user_id` = {user_id}""")
        logging.info("Value has been updated")
