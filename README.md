# Real_Estates_Recommender_System
![wesite first demo](demo_1.gif) <br>
The goal is to find estates which are shown to the user based on a recommendation system opposed to a criterion search.<br>
This repository is to serve as a base to develop and test ideas to complete the goal mention above.
<br>
<br>
## I - Gather Data
This apps is to offer to the resident of the [**Greater Paris**](https://en.wikipedia.org/wiki/Grand_Paris) so we need to gather adverts from those cities.<br>
First we search for a [website](http://comersis.fr/communes.php?epci=200054781) that contains the names of the cities of the Greater Paris. Then we proceed to collect these names into a database. This step is done in the script [_data/grand\_paris\_boroughts.py_](data/grand_paris_boroughts.py)<br>
Thanks to the name of the cities, we can make a bot that search real estates adverts in those cities in the websites that we want. We then proceed to put these adverts in a database and engineered them to a standart format to enables the gathering of data from multiples websites. These steps are done in [_data/grand\_paris\_estates.py_](data/grand_paris_estates.py), [_data/data\_validation.py_](data/data_validation.py) and [_data/data\_integration.py_](data/data_integration.py)<br>
The gathering of the data can be done at regular intervals and automated to have adverts which are up to date.<br>
(!Adverts in this repository are outdated!)
<br>
<br>
## II - Making the Website
Once we have adverts stored in a database we can make a website that will show them to the user. The website is done in the the directory [_PinEstate_](PinEstate). The website is done using django but the database used is in mongoDB because we have unstructured data, so sqlite and the model systems are not used. However we can still used this model or another if wanted to, it is a matter of opinion.<br>
The most important thing to do in the website is to save actions of each user. To do that without having our user to registered on our website, we make a cookie that stored a unique key, this key is then store in our database. At each action of our user, we store this action in our database.<br>
In this repository there is 3 actions:<br>
  - The user click on a advert to see his detail page from the home page<br>
  - The user click on the link that redirect in the original website of the advert to see more details<br>
  - The user click on an advert to see his detail page from the the page of another advert<br>

## III - Recommend adverts
<img src="demo_2.gif" alt="website second demo">

To recommend items we will use a collaborative filtering algorithm that is located in the file [_PinEstate/adverts/learning.py_](PinEstate/adverts/learning.py).
Thanks to the action of each user that are stored in the database, we can produce a score matrix whith that count actions for each user for each item. 
With this matrix we can for each user, find users that are similar and then recommend items based of the score that similar users have get to other items.
