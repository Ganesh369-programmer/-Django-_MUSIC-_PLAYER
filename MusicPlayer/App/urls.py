from django.contrib import admin
from django.urls import path , include

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    
    path('', views.index , name="index"),
    path('login' , views.loginn , name="login"),
    path('register/' , views.register , name="register"),
    path('player', views.player , name="player"),
    path('download', views.download , name="download"),
    path('/logout', views.logoutt , name="logout"),

]
