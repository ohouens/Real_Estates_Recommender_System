from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.views import generic

from .models import Estate

from .connect import Connect
from pymongo import MongoClient
from bson.objectid import ObjectId

class IndexView(generic.ListView):
    template_name = "adverts/index.html"
    context_object_name = "latest_estate_list"

    """Return the last 20 estates"""
    def get_queryset(self):
        result = []
        client = Connect.get_connection()
        db = client.grand_paris_estates_unified
        cursor = db.inventory.find({"image": {"$ne":float('nan')}})
        for inventory in cursor:
            to_add = inventory
            to_add["id"] = str(inventory["_id"])
            result.append(to_add)
        return result[:20]

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
        estate_list = result[:20]
        cursor = db.inventory.find_one({"_id":ObjectId(estate_id)})
        cursor["eperm2"] = int(int(cursor["price"][:-2].replace(" ",""))/int(cursor["size"]))
        context = {"cursor":cursor, "estate_list":estate_list}
    except Exception:
        raise Http404("Estate not found")
    return render(request, "adverts/detail.html", context)

def pin(request, estate_id):
    return HttpResponse("To pin estate %s" % estate_id)
