from django.shortcuts import render 
import pyrebase 
  
config={ 
    'apiKey': "AIzaSyCSOfSjkEoNTmMhtLrw0x2GqVMEKfwclts",
    'authDomain': "ie-hack.firebaseapp.com",
    'projectId': "ie-hack",
    'storageBucket': "ie-hack.appspot.com",
    'messagingSenderId': "529335447694",
    'appId': "1:529335447694:web:21baf2ca2203ef801459df",
    'measurementId': "G-31CQJFB6G0"
} 
firebase=pyrebase.initialize_app(config) 
auth = firebase.auth() 
database=firebase.database() 
  
def home(request): 
    day = database.child('Data').child('Day').get().val() 
    id = database.child('Data').child('Id').get().val() 
    projectname = database.child('Data').child('Projectname').get().val() 
    return render(request,"Home.html",{"day":day,"id":id,"projectname":projectname })