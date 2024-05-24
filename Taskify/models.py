from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator


def get_upload_path(instance, filename) -> str:
    return f'{instance.user.username}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=get_upload_path, default='./static/images/default_avatar.jpg', validators=[
                               FileExtensionValidator(['png', 'jpg', 'jpeg'])])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} #{self.id}'


class Task(models.Model):
    PRIORITY_STATUS = {
        "low": "Low",
        "medium": "Medium",
        "high": "High"
    }

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_STATUS)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Task#{self.id} - {self.title}'
