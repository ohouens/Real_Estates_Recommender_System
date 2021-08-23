from django.urls import path

from . import views

app_name = 'adverts'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<slug:estate_id>/', views.detail, name="detail"),
    path('<slug:estate_id>/pin/', views.pin, name="pin"),
]
