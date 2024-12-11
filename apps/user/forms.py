from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.forms import Form, CharField, EmailField

from apps.user.models import User


class LoginForm(Form):
    email = EmailField()
    password = CharField()

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise ValidationError('Email Does Not Exist')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        email = self.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if not check_password(password, user.password):
                raise ValidationError('Incorrect Password')
            else:
                return password
        return password

