from connect import Connect
from pymongo import MongoClient
from pprint import pprint

import pandas as pd

client = Connect.get_connection()
db = client.grand_paris_estates_unified

unique = ["link", "type"]

data = pd.read_csv("grand_paris_estates.csv")
to_insert = data.to_dict('records')

print(list(data.columns))
print(to_insert[0])

for advert in to_insert:
    cursor = db.inventory.find({unique[0]:advert[unique[0]], unique[1]:advert[unique[1]]})
    if(len(list(cursor)) <= 0):
        db.inventory.insert_one(advert)
