from django.shortcuts import render
from bookings.serializer import BookingSerializer
from rest_framework.viewsets import ModelViewSet
from bookings.models import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework.decorators import action
from django.utils import timezone

# Create your views here.

class BookingView(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    queryset = Booking.objects.all()

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Booking.objects.all()
        return Booking.objects.filter(user =self.request.user)

    def create(self, request, *args, **kwargs):
        dserializer = BookingSerializer(data=request.data)
        if dserializer.is_valid():
            event = dserializer.validated_data["event"]
            seats = dserializer.validated_data["seats_booked"]

            today = timezone.localdate()
            if event.date < today:
                return Response({"Error":"Cannot book a completed event"},status=status.HTTP_400_BAD_REQUEST)
            
            booked_seat = Booking.objects.filter(event=event,status="confirmed")
            booked_seat = booked_seat.aggregate(total = models.Sum("seats_booked"))["total"] or 0
            available_seat = event.total_seat - booked_seat

            if seats > available_seat:
                return Response({"error":"seats are not available","available seat":available_seat},status=status.HTTP_400_BAD_REQUEST)
            dserializer.save(user=request.user)
            send_mail(
                subject="Booking Confirmation",
                message=f"""
                Hello {request.user.username},
                Your booking has been confirmed.
                Event: {event.title}
                Seats booked: {seats}
                date :{event.date}
                time :{event.time}
                Thank you for booking with us.
                """,
                    from_email=None,
                    recipient_list=[request.user.email],
            )
            return Response(data=dserializer.data,status=status.HTTP_201_CREATED)
        return Response(data=dserializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        delete_id = self.kwargs.get("pk")
        Booking.objects.get(id=delete_id).delete()
        return Response(data={"Booking Deleted"},status=status.HTTP_200_OK)
    
    @action(methods=["delete"],detail=True)
    def cancel_booking(self,request,pk=0):
        booking = self.get_object()
        event = booking.event
        seats = booking.seats_booked
        if booking.status == "cancelled":
            return Response(data={"msg":"The booking is already cancelled"})
        booking.status ="cancelled"
        booking.save()
        send_mail(
            subject="Booking Cancelled succefully",
            message=f"""
            Hello {request.user.username},
            Your booking is cancelled.
            Event: {event.title}
            Seats booked: {seats}
            date :{event.date}
            time :{event.time}
            Thank you.
            """,
                from_email=None,
                recipient_list=[request.user.email],)
        booking.delete()
        #print(booking)
        return Response(data={"The booking is cancelled succesfully"},status=status.HTTP_200_OK)
    