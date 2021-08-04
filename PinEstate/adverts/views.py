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
        data = pd.read_csv("../data/grand_paris_estates.csv")
        subset = data[data["type"].notna()][["type", "price"]]
        subset["id"] = range(len(subset))
        subset = subset.rename(columns={"type":"title"})
        return subset.head().to_dict('records')

class DetailView(generic.DetailView):
    model = Estate
    template_name = "adverts/detail.html"

def pin(request, estate_id):
    return HttpResponse("To pin estate %s" % estate_id)
