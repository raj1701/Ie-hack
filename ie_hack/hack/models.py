from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=50, null=False,)
    desc = models.TextField(null=False)
    date = models.DateField(auto_now=True)
    mentors = models.ManyToManyField(User)
    venue = models.CharField(max_length=50,null=False)
    sig = models.CharField(max_length=20,null=True)
    active = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    

class Resource(models.Model):
    name = models.CharField(max_length=50, null=False,)
    link = models.TextField(null=False) 
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="resources")
    author= models.ForeignKey(User,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name
    

class EventRequest(models.Model):
    models.ForeignKey(Event,on_delete=models.CASCADE)
    status_choice = [
        (0,'Pending'),
        (1,'Accepted'),
        (-1,'Rejected'),
    ]
    status = models.IntegerField(
        choices=status_choice,
        default=0
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)