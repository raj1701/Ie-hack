from django.shortcuts import render, redirect
from .models import Event, Resource, EventRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        return redirect('/login_firebase')
    events = Event.objects.filter(active=True)
    return render(request, "dashboard.html",{"user": request.user , "events": events})

def create_form(request):
     return render(request,"create_form.html")

def create_event(request):
    if not request.user.is_authenticated:
        return redirect('/login_firebase')
    if not name or not desc or not venue or not sig:
        return redirect('/events')
    
    name = request.POST.get("name")    
    desc = request.POST.get("desc")    
    venue = request.POST.get("venue")    
    sig = request.POST.get("sig")
    date= request.POST.get('date')    
    event  = Event(name=name, desc= desc, venue= venue, sig=sig, date= date, active=True)
    event.save()
    current_user = User.objects.get(id = request.user.id)
    event.mentors.add(current_user)
    event.save()
    return redirect('/events')

def add_resource(request,event_id):
    event = Event.objects.get(pk =event_id)
    if request.method == "GET":
        return render(request, "add_resource.html",{"user": request.user,"event":event})
    
    if not request.user.is_authenticated:
        return redirect('/login_firebase')

    if not request.user in event.mentors.all():
        return redirect('/events')
    resource = Resource(name= request.POST.get("name"), link=request.POST.get("link"), event=event, author=request.user)  
    resource.save()
    return redirect('/events')