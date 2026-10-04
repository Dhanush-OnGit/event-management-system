from django.db import models
from events.models import Event
from django.conf import settings
# Create your models here.

class Booking(models.Model):
    status_choice=[
        ("confirmed","confirmed"),
        ("cancelled","cancelled")
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="booking")
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name="booking")
    seats_booked = models.PositiveIntegerField()
    status = models.CharField(max_length=20,choices=status_choice,default="confirmed")
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username +"-"+self.event.title