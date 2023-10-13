import datetime
import random

from pymongo import MongoClient


def add_fake_values_to_database(email: str, days: int):
    mongo = MongoClient('mongodb://127.0.0.1:27017/test')
    db = mongo['test']
    calories = db.get_collection('calories')
    for i in range(0, days + 1):
        date = datetime.date.today() - datetime.timedelta(days=i)
        calories.insert_one({'date': str(date), 'email': email, 'calories': random.randint(200, 300)})
    print("Positive Values have been added to the database")


def add_fake_negetive_values_to_database(email: str, days: int):
    mongo = MongoClient('mongodb://127.0.0.1:27017/test')
    db = mongo['test']
    calories = db.get_collection('calories')
    for i in range(0, days + 1):
        if random.randint(0, 69420) % 2 == 0:
            continue
        date = datetime.date.today() - datetime.timedelta(days=i)
        calories.insert_one({'date': str(date), 'email': email, 'calories': random.randint(-200, 0)})
    print("Negative values have been added to the database")


if __name__ == '__main__':
    add_fake_values_to_database('', 7)
    add_fake_negetive_values_to_database('', 7)
