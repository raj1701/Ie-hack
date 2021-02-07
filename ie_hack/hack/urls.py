from django.urls import path 
from . import views

urlpatterns = [
path('',views.home, name= 'index'),
path("login_firebase",views.login_firebase, name="login" ),
path("firebase_login_save",views.firebase_login_save),
path('create_form',views.create_form, name = "create_form"),    
path('create_event',views.create_event, name = "create_event"),
path('<int:event_id>/add_resource', views.add_resource, name = "add_resource"),
path('send_mail',views.send_mail),
path('logout',views.logout_user,name="logout")   
]
 