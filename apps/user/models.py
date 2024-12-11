import os

from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import *


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class UserRole(TextChoices):
        ADMIN = 'admin', 'Admin'
        USER = 'user', 'User'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    email = EmailField(unique=True, null=False, blank=False)
    username = None
    rank = PositiveSmallIntegerField(default=0)
    role = CharField(choices=UserRole.choices, default=UserRole.USER, max_length=50)

    def __str__(self):
        return self.email


class Book(Model):
    name = CharField(max_length=255)
    level = PositiveSmallIntegerField(default=1)
    image = ImageField(upload_to='books/')


class Unit(Model):
    name = CharField(max_length=255)
    unit_num = PositiveSmallIntegerField(default=1)
    book = ForeignKey(Book, related_name='units', on_delete=CASCADE)


class Vocabulary(Model):
    uzbek = CharField(max_length=255)
    english = CharField(max_length=255)
    audio = FileField(upload_to='vocabulary_audio/')
    unit = ForeignKey(Unit, related_name='vocabularies', on_delete=CASCADE)

    def delete(self, *args, **kwargs):
        if self.audio and os.path.isfile(self.audio.path):
            os.remove(self.audio.path)
        super().delete(*args, **kwargs)



class TestSection(Model):
    title = CharField(max_length=255)
    created_at = DateTimeField(auto_now_add=True)
    updated_at = DateTimeField(auto_now=True)


class Test(Model):
    class TESTCHOICES(TextChoices):
        a = 'a', 'a'
        b = 'b', 'b'
        c = 'c', 'c'
        d = 'd', 'd'

    question = CharField(max_length=255)
    a = CharField(max_length=128)
    b = CharField(max_length=128)
    c = CharField(max_length=128)
    d = CharField(max_length=128)
    correct = CharField(max_length=5, choices=TESTCHOICES.choices)
    test_section = ForeignKey(TestSection, related_name='tests', on_delete=CASCADE)


class Result(Model):
    user = ForeignKey(User, related_name='results', on_delete=CASCADE)
    unit = ForeignKey(Unit, related_name='results', on_delete=CASCADE)
    correct = SmallIntegerField()
    incorrect = SmallIntegerField()
    created_at = DateTimeField(auto_now_add=True)
