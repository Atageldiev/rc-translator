<img src="./logo.jpg" alt="RC-Translator" style="width: 100%;">

### To start this bot locally:
You will need:
- Python version: [Python 3.9](https://www.python.org/downloads/release/python-390/)
- DB: [Atlas MongoDB](https://www.mongodb.com)

Steps:
- Create a virtualenv and install requirements
- Create a `.env.dev` file where you have to pass following data:
    ```
    DB_USER=<Your MongoDB user's full name>
    DB_PASS=<MongoDB db-password>
    DB_HOST=<MongoDB host name>
    TOKEN=<Bot API Token from BotFather>
    ```
- Then run `bot.py`