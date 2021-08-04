from django.db import models

class Estate(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField(default=0)
    size = models.IntegerField(default=1)
    image = models.CharField(max_length=250)
    rooms = models.IntegerField(default=1)
    location = models.CharField(max_length=200)
    e_type = models.CharField(max_length=40)
    pub_date = models.DateTimeField("date published")

    def price_per_square_meter(self):
        return self.price/self.size

    def __str__(self):
        return self.title

class User(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=100)

class Pin(models.Model):
    estate =  models.ForeignKey(Estate, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
