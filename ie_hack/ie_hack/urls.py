from django.contrib import admin 
from django.urls import path,include 
from . import views 

urlpatterns = [ 
	path('admin/', admin.site.urls), 
	path('', views.home), 
    path("login_firebase",views.login_firebase, name="login" ),
    path("firebase_login_save",views.firebase_login_save),
    path('events/',include('hack.urls'))
] 
