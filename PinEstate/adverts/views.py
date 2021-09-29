import random
import os, binascii

from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import generic

from .models import Estate

from .connect import Connect
from pymongo import MongoClient
from bson.objectid import ObjectId

def index(request):
    """
    request:
    Home page, show a set of real estates to the user.
    Check or make an unique key as a cookie to identify the user.
    """
    result = []
    client = Connect.get_connection()
    db = client.grand_paris_estates_unified
    context = dict()
    if not request.COOKIES.get("user"):
        cursor = db.inventory.find({"image": {"$ne":float('nan')}})
        for inventory in cursor:
            to_add = inventory
            to_add["id"] = str(inventory["_id"])
            result.append(to_add)
        key = binascii.b2a_hex(os.urandom(15)).decode("utf-8")
        context = {"latest_estate_list": random.sample(result,20), "user":"000"}
        response = render(request, "adverts/index.html", context)
        response.set_cookie("user", key)
        user_db = client.grand_paris_estates_users
        user_db.inventory.insert_one({"user":key})
        return response
    else:
        cursor = db.inventory.find({"image": {"$ne":float('nan')}})
        for inventory in cursor:
            to_add = inventory
            to_add["id"] = str(inventory["_id"])
            result.append(to_add)
        context = {"latest_estate_list": random.sample(result,20), "user":request.COOKIES['user']}
        response = render(request, "adverts/index.html", context)
        return response

def detail(request, estate_id):
    try:
        client = Connect.get_connection()
        db = client.grand_paris_estates_unified
        result = []
        recommendation = db.inventory.find({"image": {"$ne":float('nan')}})
        for inventory in recommendation:
            to_add = inventory
            to_add["id"] = str(inventory["_id"])
            result.append(to_add)
        estate_list = random.sample(result,3)
        cursor = db.inventory.find_one({"_id":ObjectId(estate_id)})
        cursor["rooms"] = int(cursor["rooms"])
        cursor["id"] = str(cursor["_id"])
        cursor["eperm2"] = int(int(cursor["price"][:-2].replace(" ",""))/int(cursor["size"]))
        context = {"cursor":cursor, "estate_list":estate_list}
    except Exception:
        raise Http404("Estate not found")
    return render(request, "adverts/detail.html", context)

def pin(request, estate_id):
    return HttpResponse("To pin estate %s" % estate_id)

def join(request, estate_id, target_id):
    """
    request:
    estate_id: the ID of the item of the page the user is
    target_id: The ID of the item the user click on
    Add the click action from one item to another item of an user
    in the database.
    """
    #Connect to the mongodb to be able to update add the action
    client = Connect.get_connection()
    db = client.grand_paris_estates_users
    #check if the user is new or already have an array of actions
    if not request.COOKIES.get("user"):
        pass
    #Find the user first and his array of actions item-item
    user_id = request.COOKIES["user"]
    cursor = db.inventory.find_one({"user":user_id})
    #Update the database to add the action from this user
    items_history = dict()
    if("action" in cursor and "items_history" in cursor["action"]):
        items_history = cursor["action"]["items_history"]
        if(estate_id in items_history):
            items_history[estate_id].append(target_id)
        else:
            items_history[estate_id] = [target_id]
    else:
        items_history[estate_id] = [target_id]
    db.inventory.update_one(
        {"user":user_id},
        {"$set": {"action.items_history":items_history}}
    )
    return HttpResponse("user {} saved {} to {}".format(user_id, estate_id, target_id))

def view(request, estate_id):
    """
    request:
    estate_id: the ID of the item of the page the user is
    Add the click action of the user to see the original content of the
    item in the database
    """
    client = Connect.get_connection()
    db = client.grand_paris_estates_users
    if not request.COOKIES.get("user"):
        pass
    #Find the user first and his array of actions item-item
    user_id = request.COOKIES["user"]
    cursor = db.inventory.find_one({"user":user_id})
    #Update the database to add the action from this user
    views_history = dict()
    if("action" in cursor and "views_history" in cursor["action"]):
        views_history = cursor["action"]["views_history"]
        views_history.append(estate_id)
    else:
        views_history = [estate_id]
    db.inventory.update_one(
        {"user":user_id},
        {"$set": {"action.views_history":views_history}}
    )
    return HttpResponse("user {} views {}".format(user_id, estate_id))
