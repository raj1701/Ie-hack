from django.shortcuts import render, redirect
from .models import Event, Resource, EventRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import json
from django.contrib import messages
from django.core import serializers
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import Context
from django.template.loader import get_template
from django.urls import reverse
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from io import StringIO, BytesIO
from requests import request
from ie_hack import settings
from ie_hack.settings import EMAIL_HOST_USER
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
import pyrebase 

import firebase_admin
from firebase_admin import credentials, firestore
# firebase admin
cred = credentials.Certificate("ie_hack/credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

config={ 
    'apiKey': "AIzaSyCSOfSjkEoNTmMhtLrw0x2GqVMEKfwclts",
    'authDomain': "ie-hack.firebaseapp.com",
    'projectId': "ie-hack",
    'databaseURL': "https://ie-hack-default-rtdb.firebaseio.com/", 
    'storageBucket': "ie-hack.appspot.com",
    'messagingSenderId': "529335447694",
    'appId': "1:529335447694:web:21baf2ca2203ef801459df",
    'measurementId': "G-31CQJFB6G0"
} 
firebase=pyrebase.initialize_app(config) 
auth = firebase.auth() 
database=firebase.database() 
# Create your views here.
# def home(request): 
#     day = database.child('Data').child('Day').get().val() 
#     id = database.child('Data').child('Id').get().val() 
#     projectname = database.child('Data').child('Projectname').get().val() 
#     return render(request,"Home.html",{"day":day,"id":id,"projectname":projectname })
username=""
email=""

def login_firebase(request):
    return render(request,"login_firebase.html")


@csrf_exempt
def firebase_login_save(request):
    global username
    global email
    username=request.POST.get("username")
    email=request.POST.get("email")
    provider=request.POST.get("provider")
    token=request.POST.get("token")
    firbase_response=loadDatafromFirebaseApi(token)
    firbase_dict=json.loads(firbase_response)
    if "users" in firbase_dict:
        user=firbase_dict["users"]
        if len(user)>0:
            user_one=user[0]
            if "phoneNumber" in user_one:
                if user_one["phoneNumber"]==email:
                    data=proceedToLogin(request,email, username, token, provider)
                    return HttpResponse(data)
                else:
                    return HttpResponse("Invalid Login Request")
            else:
                if email==user_one["email"]:
                    provider1=user_one["providerUserInfo"][0]["providerId"]
                    if user_one["emailVerified"]==1 or user_one["emailVerified"]==True or user_one["emailVerified"]=="True" or provider1=="facebook.com":
                        data=proceedToLogin(request,email,username,token,provider)
                        return HttpResponse(data)
                    else:
                        return HttpResponse("Please Verify Your Email to Get Login")
                else:
                    return HttpResponse("Unknown Email User")
        else:
            return HttpResponse("Invalid Request User Not Found")
    else:
        return HttpResponse("Bad Request")


def loadDatafromFirebaseApi(token):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:lookup"

    payload = 'key=AIzaSyCSOfSjkEoNTmMhtLrw0x2GqVMEKfwclts&idToken='+token
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = request("POST", url, headers=headers, data=payload)

    return response.text


def proceedToLogin(request,email,username,token,provider):
    users=User.objects.filter(username=username).exists()

    if users==True:
        user_one=User.objects.get(username=username)
        user_one.backend='django.contrib.auth.backends.ModelBackend'
        login(request,user_one)
        return "login_success"
    else:
        user=User.objects.create_user(username=username,email=email,password=settings.SECRET_KEY)
        user_one=User.objects.get(username=username)
        user_one.backend='django.contrib.auth.backends.ModelBackend'
        login(request,user_one)
        return "login_success"


def home(request):
    if not request.user.is_authenticated:
        return redirect('/login_firebase')
    events = Event.objects.filter(active=True)
    docs = db.collection('users').where("email", "==", email).get()
    if docs:
        pass
    else:
        data = {
            "Name": username,
            "email":email,
        }
        db.collection('users').add(data)
    
    return render(request, "dashboard.html",{"user": request.user , "events": events,"username":username})



def create_form(request):
     return render(request,"create_form.html")



def create_event(request):
    if not request.user.is_authenticated:
        return redirect('/login_firebase')

    
    name = request.POST.get("name")    
    desc = request.POST.get("desc")    
    venue = request.POST.get("venue")    
    sig = request.POST.get("sig")
    date= request.POST.get('date')  
    if not name or not desc or not venue or not sig:
        return redirect('/')
    event  = Event(name=name, desc= desc, venue= venue, sig=sig, date= date, active=True)
    event.save()
    current_user = User.objects.get(id = request.user.id)
    event.mentors.add(current_user)
    event.save()
    return redirect('/')

def add_resource(request,event_id):
    event = Event.objects.get(pk =event_id)
    if request.method == "GET":
        return render(request, "add_resource.html",{"user": request.user,"event":event})
    
    if not request.user.is_authenticated:
        return redirect('/login_firebase')

    if not request.user in event.mentors.all():
        return redirect('/')
    resource = Resource(name= request.POST.get("name"), link=request.POST.get("link"), event=event, author=request.user)  
    resource.save()
    return redirect('/')
    
