import django_filters
from .models import Task, Profile
from django.contrib.auth.models import User


class TaskFilter(django_filters.FilterSet):

    class Meta:
        model = Task
        fields = {
            'title': ['contains'],
            'priority': ['exact'],
            'status': ['exact'],
            'created_at': ['lt'],
        }
