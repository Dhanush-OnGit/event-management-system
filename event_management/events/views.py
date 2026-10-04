from django.shortcuts import render
from events import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from events.serializer import *
from events.permissions import IsSuperUser
from django.utils import timezone
from datetime import timedelta
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.

class CategoryView(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class EventView(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend]
    search_fields = ["title","venue"]
    filterset_fields = ["category","status"]
    #queryset = Event.objects.all()

    def get_queryset(self):
        today = timezone.localdate()
        events = Event.objects.filter(date__lt=today,status__in=["upcoming","Today","Tomorrow"])
        events.update(status="completed")
        return Event.objects.all()

    # def get_permissions(self):
    #     if self.action in ["update","partial_update","destroy"]:
    #         return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        dserializer = EventSerializer(data = request.data)
        if dserializer.is_valid():
            event = dserializer.save(owner = request.user)
            today = timezone.localdate()
            if event.date <today:
                event.status = "completed"
            elif event.date == today:
                event.status = "Today"
            elif event.date == today + timedelta(days=1):
                event.status = "Tomorrow"
            else:
                event.status = "upcoming"
            event.save()

            #dserializer.save(owner = request.user)
            return Response(data=dserializer.data,status=status.HTTP_201_CREATED)
        return Response(data=dserializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def update(self,request,*args,**kwargs):
        event = self.get_object()
        dserializer = EventSerializer(event,data = request.data,partial = True)
        if dserializer.is_valid():
            event = dserializer.save(owner = request.user)
            today = timezone.localdate()
            if event.date <today:
                event.status = "completed"
            elif event.date == today:
                event.status = "Today"
            elif event.date == today + timedelta(days=1):
                event.status = "Tomorrow"
            else:
                event.status = "upcoming"
            event.save()
            return Response(data=dserializer.data,status=status.HTTP_201_CREATED)
        return Response(data=dserializer.errors,status=status.HTTP_400_BAD_REQUEST)

    
    