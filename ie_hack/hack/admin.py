from django.contrib import admin
from .models import Event, Resource, EventRequest
# Register your models here.
admin.register(Resource)
admin.register(Event)
admin.register(EventRequest)