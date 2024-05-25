from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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
