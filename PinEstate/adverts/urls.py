from django.urls import path

from . import views

app_name = 'adverts'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name="detail"),
    path('<int:estate_id>/pin/', views.pin, name="pin"),
]
