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
