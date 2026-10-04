from django.shortcuts import render
from accounts.models import *
from accounts.serializer import UserSerializer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

# Create your views here.
class SignInView(ViewSet):
    def create(self,request):
        deserialization = UserSerializer(data = request.data)
        if deserialization.is_valid():
            deserialization.save()
            return Response(data=deserialization.data,status=status.HTTP_201_CREATED)
        return Response(data=deserialization.errors,status=status.HTTP_400_BAD_REQUEST)

class LoginView(ViewSet):
    def create(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username,password=password)
        if user:
            token,created = Token.objects.get_or_create(user=user)
            return Response(data={"msg":"Login succesfull","user_id":user.id,"token":token.key,"username":user.username},status=status.HTTP_201_CREATED)
        return Response(data={"error"},status=status.HTTP_400_BAD_REQUEST)