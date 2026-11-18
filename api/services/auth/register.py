from django import forms
from django.core.exceptions import ValidationError
from service_objects.services import ServiceWithResult
from models_app.models import User


class UserRegisterService(ServiceWithResult):
    username = forms.CharField(max_length=150)
    email = forms.EmailField(required=False)
    password = forms.CharField(min_length=8)
    password_confirm = forms.CharField(min_length=8)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        return username


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Пароли не совпадают.")
        return cleaned_data

    def process(self):
        if self.is_valid():
            self.result = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data.get('email') or '',
                password=self.cleaned_data['password'],
            )
        return self