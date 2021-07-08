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
        estate['doors'] = specs[0].get_text()
        estate['rooms'] = specs[1].get_text()
        estate['size'] = specs[2].get_text()
        print(estate['doors'])
        print(estate['rooms'])
        print(estate['size'])

    #city
    # estate['city'] =

    #image
    # estate['image'] =

    #description
    # estate['description'] =

    estates.append(estate)
