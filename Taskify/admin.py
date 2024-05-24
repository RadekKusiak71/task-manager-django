from django.contrib import admin
from .models import Task, Profile


admin.site.register(Profile)
admin.site.register(Task)
