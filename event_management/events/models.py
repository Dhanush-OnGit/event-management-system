from django.db import models
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    describtion = models.CharField(blank=True)
    def __str__(self):
        return self.name

class Event(models.Model):
    status_choice = [
        ("upcoming", "Upcoming"),
        ("completed", "Completed"),
        ("Today","Today"),
        ("Tomorrow","Tomorrow")
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="events")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="events")
    title = models.CharField(max_length=100)
    discription = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=100)
    total_seat = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=status_choice,max_length=20,default="upcoming")
    def __str__(self):
        return self.title