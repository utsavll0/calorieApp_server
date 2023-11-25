from apps import App
import pandas as pd

app = App()
mongo = app.mongo

# Clear existing data in the 'food' and 'obesity' collections
mongo.db.food.delete_many({})
mongo.db.obesity.delete_many({})

# Food Data
f = open('food_data/calories.csv', 'r', encoding="ISO-8859-1")
l = f.readlines()

for i in range(1, len(l)):
    l[i] = l[i][1:len(l[i]) - 2]

for i in range(1, len(l)):
    temp = l[i].split(",")
    mongo.db.food.insert_one({'food': temp[0], 'calories': temp[1]})

# BMI data
df = pd.read_csv('model/WHO_obesityByCountry_2016.csv')

for index, row in df.iterrows():
    country_name = row['Country']
    both_sexes = row['Both.sexes'] 
    male = row['Male']
    female = row['Female']

    mongo.db.obesity.insert_one({
        'country_name': country_name,
        'both_sexes': both_sexes,
        'male': male,
        'female': female
    })

print("Data inserted into MongoDB.")