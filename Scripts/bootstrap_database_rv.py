import datetime
import random

from pymongo import MongoClient


def add_fake_values_to_database(email: str, days: int):
    mongo = MongoClient('mongodb://127.0.0.1:27017/test')
    db = mongo['test']
    calories = db.get_collection('calories')
    for i in range(0, days + 1):
        date = datetime.date.today() - datetime.timedelta(days=i)
        calories.insert_one({
            'date': str(date),
            'email': email,
            'calories': random.randint(2100, 2300)
        })
    print("Positive Values have been added to the database")


def add_fake_negetive_values_to_database(email: str, days: int):
    mongo = MongoClient('mongodb://127.0.0.1:27017/test')
    db = mongo['test']
    calories = db.get_collection('calories')
    for i in range(0, days + 1):
        if random.randint(0, 69420) % 2 == 0:
            continue
        date = datetime.date.today() - datetime.timedelta(days=i)
        calories.insert_one({
            'date': str(date),
            'email': email,
            'calories': random.randint(-500, 0)
        })
    print("Negative values have been added to the database")


def clear_calories_db():
    mongo = MongoClient('mongodb://127.0.0.1:27017/test')
    db = mongo['test']
    calories = db.get_collection('calories')
    calories.delete_many({})


if __name__ == '__main__':
    # Add email and database will be populated with random values for that email
    add_fake_values_to_database('', 30)
    add_fake_negetive_values_to_database('', 30)

    # Uncomment this line to clear calories collection
    # clear_calories_db()
