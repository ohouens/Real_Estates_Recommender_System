from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.views import generic

from .models import Estate

class IndexView(generic.ListView):
    template_name = "adverts/index.html"
    context_object_name = "latest_estate_list"

    """Return the last 5 estates"""
    def get_queryset(self):
        return Estate.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Estate
    template_name = "adverts/detail.html"

def pin(request, estate_id):
    return HttpResponse("To pin estate %s" % estate_id)
