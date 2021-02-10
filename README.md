### To start this bot locally:
You will need:
- Python version: [Python 3.9](https://www.python.org/downloads/release/python-390/)
- DB: [Atlas MongoDB](https://www.mongodb.com)

Steps:
- Create a virtualenv and install requirements
- create a `.env.dev` file where you will have to pass following data:
    ```
    DB_USER=<Your MongoDB user's full name>
    DB_PASS=<MongoDB db-password>
    DB_DB=<MongoDB database name>
    TOKEN=<Bot API Token from BotFather>
    ```
- Then run `bot.py`