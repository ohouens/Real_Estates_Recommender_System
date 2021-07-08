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
# features: size, price, city, image, link, description
estates = []
for ad in ads:
    estate = {}

    #type
    # estate['type'] =

    #price
    price = ad.find(class_="Price__Label-sc-1g9fitq-1")
    if(price != None):
        estate['price'] = price.get_text()
        print(price.get_text())

    #size
    # estate['size'] =

    #city
    # estate['city'] =

    #image
    # estate['image'] =

    #description
    # estate['description'] =

    estates.append(estate)
