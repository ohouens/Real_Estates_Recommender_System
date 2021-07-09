import time
import requests
import mechanicalsoup
import pandas as pd

from connect import Connect
from pymongo import MongoClient

client = Connect.get_connection()
db = client.grand_paris_estates

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'}
racine = "https://www.seloger.com/immobilier/achat/"
boroughts = pd.read_csv('grand_paris_boroughts.csv')
feuilles = ["bien-appartement/", "bien-maison/"]
browser = mechanicalsoup.Browser()
for index, row in boroughts.iterrows():
    for feuille in feuilles:
        URL = racine+"immo-"+"".join(row['name'].lower().split())+"-"+str(row['department'])+"/"+feuille
        URL = URL.replace(" ", "")
        # print(URL)
        # exit()

        done = False
        while(not done):
            page = browser.get(URL, headers=headers)
            if(page.status_code == 404):
                print("empty city")
                continue
            # print(page)
            # print(type(page.soup))
            # print(page.soup)
            soup = page.soup
            ads = soup.find_all(class_="ListContent-sc-1viyr2k-0")

            # build the dict to insert in the databse
            # features: size, door, rooms, price, city, image, link, description
            for ad in ads:
                print("-"*70)
                estate = {}

                #type
                estate['type'] = ""
                type_ = ad.find(class_="ContentZone__Title-wghbmy-5")
                if(type_ != None):
                    estate['type'] = type_.get_text()
                    print(estate['type'])

                #price
                estate['price'] = ""
                price = ad.find(class_="Price__Label-sc-1g9fitq-1")
                if(price != None):
                    estate['price'] = price.get_text()
                    print(price.get_text())

                #size, rooms, doors
                estate['doors'] = ""
                estate['rooms'] = ""
                estate['size'] = ""
                specs = ad.find("ul")
                if(specs != None):
                    specs = specs.find_all('li')
                    if(len(specs) >= 1):
                        estate['doors'] = specs[0].get_text()
                        print(estate['doors'])
                    if(len(specs) >= 2):
                        estate['rooms'] = specs[1].get_text()
                        print(estate['rooms'])
                    if(len(specs) >= 3):
                        estate['size'] = specs[2].get_text()
                        print(estate['size'])

                #city
                estate['city'] = ""
                estate['zone'] = ""
                city = ad.find(class_="ContentZone__Address-wghbmy-1 dlWlag")
                if(city != None):
                    estate['city'] = city.find("span").get_text()
                    print(estate['city'])
                    zone = city.find_all("span")
                    if(len(zone) >= 2):
                        estate['zone'] = zone[1].get_text()
                        print(estate['zone'])

                #image
                estate['image'] = ""
                image = ad.find('img')
                if(image != None):
                    estate['image'] = image['src']
                    print(estate['image'])

                #description
                estate['description'] = ""
                desc = ad.find(class_='Card__Description-sc-7insep-6')
                if(desc != None):
                    estate['description'] = desc.get_text()
                    print(estate['description'])

                #link
                estate['link'] = ""
                link = ad.find(class_="CoveringLink-a3s3kt-0")
                if(link != None):
                    estate['link'] = link["href"]
                    print(estate['link'])

                db.inventory.insert_one(estate)

            time.sleep(1)
            next_page = soup.find(class_="next")
            if(next_page != None):
                URL = "https://www.seloger.com"+next_page.find("a")["href"]
                print(URL)
            else:
                done = True
