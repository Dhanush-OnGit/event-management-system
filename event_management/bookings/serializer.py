from rest_framework import serializers
from bookings.models import *

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    event_title = serializers.CharField(source="event.title",read_only=True)
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["id","status","booking_date","user","event_title"]

    def validate_seats_booked(self,value):
        if value <=0:
            raise serializers.ValidationError("Seats booked must be greater than 0.")
        return value