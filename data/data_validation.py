import pandas as pd
import numpy as np

from connect import Connect
from pymongo import MongoClient
from pprint import pprint

client = Connect.get_connection()
db = client.grand_paris_estates

cursor = db.inventory.find({})

#init columns
city = []
description = []
doors = []
image = []
link = []
price = []
rooms = []
size = []
type = []
zone = []


for inventory in cursor:
    # pprint(inventory)
    city.append(inventory['city'])
    description.append(inventory['description'])
    doors.append(inventory['doors'])
    image.append(inventory['image'])
    link.append(inventory['link'])
    price.append(inventory['rooms'])
    size.append(inventory['size'])
    type.append(inventory['type'])
    zone.append(inventory['zone'])

d = {
        'city': city,
        'description': description,
        'doors': doors,
        'image': image,
        'link': link,
        'price': price,
        'size': size,
        'type': type,
        'zone': zone
    }
data_to_csv = pd.DataFrame(data=d)
data_to_csv.to_csv("grand_paris_estates.csv")

print(data_to_csv.head())
