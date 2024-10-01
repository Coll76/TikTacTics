from django.db import models
from django.contrib.auth.models import User, AbstractUser, AbstractBaseUser #new
from django.utils import timezone #new

class User(AbstractUser):

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    #password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

class PhishingLink(models.Model):

    url = models.URLField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class PhishingData(models.Model):

    link = models.ForeignKey(PhishingLink, on_delete=models.CASCADE)
    phishing = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
