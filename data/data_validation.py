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
zipcode = []
description = []
image = []
link = []
price = []
rooms = []
bedrooms = []
size = []
estate_type = []
zone = []


for inventory in cursor:
    # pprint(inventory)
    city.append(inventory['city'])
    description.append(inventory['description'])
    image.append(inventory['image'])
    link.append(inventory['link'])
    price.append(inventory['price'])
    estate_type.append(inventory['type'])
    zone.append(inventory['zone'])

    b = None
    r = None
    s = None

    if(len(inventory['doors'].split()) > 1):
        if(inventory['doors'].split()[1] == "p"):
            r = inventory['doors'].split()[0]
        if(inventory['doors'].split()[1] == "ch"):
            b = inventory['doors'].split()[0]
        if(inventory['doors'].split()[1] == "m²"):
            s = inventory['doors'].split()[0]

    if(len(inventory['rooms'].split()) > 1):
        if(inventory['rooms'].split()[1] == "p"):
            r = inventory['rooms'].split()[0]
        if(inventory['rooms'].split()[1] == "ch"):
            b = inventory['rooms'].split()[0]
        if(inventory['rooms'].split()[1] == "m²"):
            s = inventory['rooms'].split()[0]

    if(len(inventory['size'].split()) > 1):
        if(inventory['size'].split()[1] == "p"):
            r = inventory['size'].split()[0]
        if(inventory['size'].split()[1] == "ch"):
            b = inventory['size'].split()[0]
        if(inventory['size'].split()[1] == "m²"):
            s = inventory['size'].split()[0]

    bedrooms.append(b)
    rooms.append(r)
    size.append(s)

d = {
        'city': city,
        'description': description,
        'image': image,
        'link': link,
        'price': price,
        'bedrooms': bedrooms,
        'rooms': rooms,
        'size': size,
        'type': estate_type,
        'zone': zone
    }
data_to_csv = pd.DataFrame(data=d)
data_to_csv.to_csv("grand_paris_estates.csv")

print(data_to_csv[["bedrooms", "rooms", "size"]].head())
