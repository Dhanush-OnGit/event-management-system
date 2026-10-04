"""
URL configuration for event_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from accounts.views import SignInView,LoginView
from events.views import CategoryView,EventView
from rest_framework.authtoken.views import obtain_auth_token
from bookings.views import *

router = DefaultRouter()

router.register('signin',SignInView,basename="signin")
router.register('category',CategoryView,basename="category")
router.register("event",EventView,basename="event")
router.register('booking',BookingView,basename="booking")
router.register('login',LoginView,basename="login")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token',obtain_auth_token),
]+router.urls
