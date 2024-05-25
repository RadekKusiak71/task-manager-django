from typing import Any, Mapping
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.base import File
from django.core.validators import FileExtensionValidator
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):

    avatar = forms.ImageField(validators=[
        FileExtensionValidator(['png', 'jpg', 'jpeg'])])

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "avatar")

    def __init__(self, *args, **kwargs) -> None:
        self.user_id = kwargs.pop("user_id")
        super().__init__(*args, **kwargs)
        self.fields['username'].required = False
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['email'].required = False
        self.fields['avatar'].required = False

    def clean_username(self):
        username = self.cleaned_data['username']
        queryset = User.objects.filter(username=username)

        if queryset.exists() and self.user_id != queryset.first().id:
            raise ValidationError("Username is already taken")

        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        queryset = User.objects.filter(email=email)

        if queryset.exists() and self.user_id != queryset.first().id:
            raise ValidationError("Email is already taken")

        return email

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if not avatar:
            avatar = Profile.objects.get(
                user__id=self.user_id)._meta.get_field("avatar").get_default()
        return avatar

    def save(self, commit=True) -> User:
        user = User.objects.get(id=self.user_id)

        for field in self.cleaned_data:
            if field != 'avatar':
                setattr(user, field, self.cleaned_data[field])

        if commit:
            user.save()

            if 'avatar' in self.cleaned_data:
                profile = Profile.objects.get(user=user)
                profile.avatar = self.cleaned_data['avatar']
                profile.save()

        return user


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=120, required=True)
    last_name = forms.CharField(max_length=120, required=True)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", 'first_name', "last_name",
                  "email", "password1", "password2")

    def clean_password2(self) -> str:
        password = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password != password2:
            raise ValidationError("password don't match")
        return password

    def clean_email(self) -> str:
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise ValidationError("A user with that email already exists")
        return self.cleaned_data['email']

    def save(self, commit=True) -> User:
        user = User.objects.create_user(username=self.cleaned_data['username'],
                                        email=self.cleaned_data['email'],
                                        password=self.cleaned_data['password1'])

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        return user
