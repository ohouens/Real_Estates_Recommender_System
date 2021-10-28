# Real_Estates_Recommender_System
![wesite first demo](demo_1.gif) <br>
The purpose of this repository is to find estate properties which are shown to the user based on a recommendation system instead of a criterion search.<br>
This repository is to serve as a base to develop and test ideas to complete the goal mentionned above.
<br>
<br>
## I - Gather Data
This application was created to help resident of [**Greater Paris**](https://en.wikipedia.org/wiki/Grand_Paris) thus adverts were gathered from cities in this region.<br>
First we searched for a [website](http://comersis.fr/communes.php?epci=200054781) that contains the names of the cities of Greater Paris. We then proceeded to collect these names into a database. This step was achieved using the the script [_data/grand\_paris\_boroughts.py_](data/grand_paris_boroughts.py)<br>
Using the names of the cities, a bot could be created to search real estate adverts in cities using relevant websites. We then proceeded to put these adverts into a database and engineered them to a standart format to enable the gathering of data from multiple websites. These steps were undertaken in [_data/grand\_paris\_estates.py_](data/grand_paris_estates.py), [_data/data\_validation.py_](data/data_validation.py) and [_data/data\_integration.py_](data/data_integration.py)<br>
The gathering of the data could be done at regular intervals and automated to have adverts which are up to date.<br>
(!Adverts in this repository are outdated!)
<br>
<br>
## II - Making the Website
Once we have adverts stored in a database we can make a website that will show them to the user. The website is created in the the directory [_PinEstate_](PinEstate). The website is created using django however the database used is in mongoDB because we have unstructured data, so sqlite and the model systems are not used. However we can still used this model or another if desired, it is a matter of choice.<br>
The most important thing to do in the website is to save events of each user. To do it without user registration, we make a cookie that stores a unique key, this key is then stored in our database. With each user's event, we store this event in our database.<br>
In this repository there are 3 events:<br>
  - The user clicks on a advert to see the page with further details from the home page<br>
  - The user clicks on the link that redirects to the original website of the advert to see more details<br>
  - The user clicks on an advert to see the page with further details from the the page of another advert<br>

## III - Recommend adverts
<img src="demo_2.gif" alt="website second demo">

To recommend items we used a collaborative filtering algorithm that is located in the file [_PinEstate/adverts/learning.py_](PinEstate/adverts/learning.py).
Using the event of each user that is stored in the database, we can produce a score matrix to count events for each user for each item. 
With this matrix we can, for each user, find users that are similar by computing the cosine similarity between users based off the N preferred items of the original user from whom we want to recommend items.<br> 
Then we recommend new items to this user based off the score that similar users gave to other items.
