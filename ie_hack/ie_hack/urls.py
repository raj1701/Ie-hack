from django.contrib import admin 
from django.urls import path 
from . import views 

urlpatterns = [ 
	path('admin/', admin.site.urls), 
	path('', views.home), 
    path("login_firebase",views.login_firebase),
    path("firebase_login_save",views.firebase_login_save)
] 
