from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views import generic

from .models import Estate

from .connect import Connect
from pymongo import MongoClient

import pandas as pd
import numpy as np

class IndexView(generic.ListView):
    template_name = "adverts/index.html"
    context_object_name = "latest_estate_list"

    """Return the last 5 estates"""
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

class DetailView(generic.DetailView):
    model = Estate
    template_name = "adverts/detail.html"

def pin(request, estate_id):
    return HttpResponse("To pin estate %s" % estate_id)
