import requests
import mechanicalsoup

URL = "https://www.seloger.com/immobilier/achat/immo-clichy-92/bien-appartement/"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'}
browser = mechanicalsoup.Browser()
page = browser.get(URL, headers=headers)

print(page)
print(type(page.soup))
# print(page.soup)
soup = page.soup
ads = soup.find_all(class_="ListContent-sc-1viyr2k-0")

# build the dict to insert in the databse
# features: size, door, rooms, price, city, image, link, description
estates = []
for ad in ads:
    print("-"*70)
    estate = {}

    #type
    type_ = ad.find(class_="ContentZone__Title-wghbmy-5")
    if(type_ != None):
        estate['type'] = type_.get_text()
        print(estate['type'])

    #price
    price = ad.find(class_="Price__Label-sc-1g9fitq-1")
    if(price != None):
        estate['price'] = price.get_text()
        print(price.get_text())

    #size, rooms, doors
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
    city = ad.find(class_="ContentZone__Address-wghbmy-1 dlWlag")
    if(city != None):
        estate['city'] = city.find("span").get_text()
        print(estate['city'])

    #zone
    

    #image
    image = ad.find('img')
    if(image != None):
        estate['image'] = image['src']
        print(estate['image'])

    #description
    desc = ad.find(class_='Card__Description-sc-7insep-6')
    if(desc != None):
        estate['description'] = desc.get_text()
        print(estate['description'])

    estates.append(estate)
