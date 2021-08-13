from django.urls import path

from . import views

app_name = 'adverts'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<slug:pk>/', views.DetailView.as_view(), name="detail"),
    path('<slug:estate_id>/pin/', views.pin, name="pin"),
]
