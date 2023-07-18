from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser

"""
User table with nick
Args: AbstractUser: username,first_name,last_name,email,password,groups,user_permissions,is_staff,is_active,is_superuser,last_login,date_joined
"""
class User(AbstractUser):
        email = models.EmailField(unique=True)
        public_key1 = models.TextField(null=True)
        public_key2 = models.TextField(null=True)

"""
Nuevos Models para la firma
"""
class Document(models.Model):
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name='creator')
    title = models.TextField()
    content = models.TextField()
    sign = models.TextField(null=True, blank=True)
    request_to = models.ForeignKey('User', on_delete=models.CASCADE, related_name='request_to')
    accepted = models.IntegerField()
    file_txt = models.FileField(null=True, blank=True)
    def __str__(self):
        return self.title